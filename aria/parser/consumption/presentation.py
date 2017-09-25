# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ...utils.formatting import (json_dumps, yaml_dumps)
from ..loading import UriLocation
from ..presentation import PresenterNotFoundError
from .consumer import Consumer


PRESENTATION_CACHE = {}
CANONICAL_LOCATION_CACHE = {}


class Read(Consumer):
    """
    Reads the presentation, handling imports recursively.

    It works by consuming a data source via appropriate :class:`~aria.parser.loading.Loader`Entry,
    :class:`~aria.parser.reading.Reader`, and :class:`~aria.parser.presentation.Presenter`
    instances.

    It supports agnostic raw data composition for presenters that have
    ``_get_import_cache`` and ``_merge_import``.

    To improve performance, loaders are called asynchronously on separate threads.

    Note that parsing may internally trigger more than one loading/reading/presentation
    cycle, for example if the agnostic raw data has dependencies that must also be parsed.
    """

    def __init__(self, context):
        super(Read, self).__init__(context)
        self._cache = {}

    def consume(self):
        main, entries = self._present_all()

        # Merge presentations
        main.merge(entries, self.context)

        # Cache merged presentations
        if self.context.presentation.cache:
            for presentation in entries:
                presentation.cache()

        self.context.presentation.presenter = main.presentation
        if main.canonical_location is not None:
            self.context.presentation.location = main.canonical_location

    def dump(self):
        if self.context.has_arg_switch('yaml'):
            indent = self.context.get_arg_value_int('indent', 2)
            raw = self.context.presentation.presenter._raw
            self.context.write(yaml_dumps(raw, indent=indent))
        elif self.context.has_arg_switch('json'):
            indent = self.context.get_arg_value_int('indent', 2)
            raw = self.context.presentation.presenter._raw
            self.context.write(json_dumps(raw, indent=indent))
        else:
            self.context.presentation.presenter._dump(self.context)

    def _handle_exception(self, e):
        if isinstance(e, _Skip):
            return
        super(Read, self)._handle_exception(e)

    def _present_all(self):
        location = self.context.presentation.location

        if location is None:
            self.context.validation.report('Presentation consumer: missing location')
            return

        executor = self.context.presentation.create_executor()
        try:
            main = self._present(location, None, None, executor)
            executor.drain()

            # Handle exceptions
            for e in executor.exceptions:
                self._handle_exception(e)

            entries = executor.returns or []
        finally:
            executor.close()

        entries.insert(0, main)

        return main, entries

    def _present(self, location, origin_canonical_location, origin_presenter_class, executor):
        # Link the context to this thread
        self.context.set_thread_local()

        # Canonicalize the location
        if self.context.reading.reader is None:
            loader, canonical_location = self._create_loader(location, origin_canonical_location)
        else:
            # If a reader is specified in the context then we skip loading
            loader = None
            canonical_location = location

        # Skip self imports
        if canonical_location == origin_canonical_location:
            raise _Skip()

        if self.context.presentation.cache:
            # Is the presentation in the global cache?
            try:
                presentation = PRESENTATION_CACHE[canonical_location]
                return _Entry(presentation, canonical_location, origin_canonical_location)
            except KeyError:
                pass

        try:
            # Is the presentation in the local cache?
            presentation = self._cache[canonical_location]
            return _Entry(presentation, canonical_location, origin_canonical_location)
        except KeyError:
            pass

        # Create and cache new presentation
        presentation = self._create_presentation(canonical_location, loader,
                                                 origin_presenter_class)
        self._cache[canonical_location] = presentation

        # Submit imports to executor
        if hasattr(presentation, '_get_import_locations'):
            import_locations = presentation._get_import_locations(self.context)
            if import_locations:
                for import_location in import_locations:
                    import_location = UriLocation(import_location)
                    executor.submit(self._present, import_location, canonical_location,
                                    presentation.__class__, executor)

        return _Entry(presentation, canonical_location, origin_canonical_location)

    def _create_loader(self, location, origin_canonical_location):
        loader = self.context.loading.loader_source.get_loader(self.context.loading, location,
                                                               origin_canonical_location)

        canonical_location = None

        # Because retrieving the canonical location can be costly, we will cache it
        cache_key = None
        if origin_canonical_location is not None:
            cache_key = (origin_canonical_location, location)

        if cache_key is not None:
            try:
                canonical_location = CANONICAL_LOCATION_CACHE[cache_key]
            except KeyError:
                pass

        if canonical_location is None:
            canonical_location = loader.get_canonical_location()
            if cache_key is not None:
                CANONICAL_LOCATION_CACHE[cache_key] = canonical_location

        return loader, canonical_location

    def _create_presentation(self, canonical_location, loader, default_presenter_class):
        # The reader we specified in the context will override
        reader = self.context.reading.reader

        if reader is None:
            # Read raw data from loader
            reader = self.context.reading.reader_source.get_reader(self.context.reading,
                                                                   canonical_location, loader)

        raw = reader.read()

        # Wrap raw data in presenter class
        if self.context.presentation.presenter_class is not None:
            # The presenter class we specified in the context will override
            presenter_class = self.context.presentation.presenter_class
        else:
            try:
                presenter_class = self.context.presentation.presenter_source.get_presenter(raw)
            except PresenterNotFoundError:
                if default_presenter_class is None:
                    raise
                else:
                    presenter_class = default_presenter_class

        if presenter_class is None:
            raise PresenterNotFoundError(u'presenter not found: {0}'.format(canonical_location))

        presentation = presenter_class(raw=raw)

        if hasattr(presentation, '_link_locators'):
            presentation._link_locators()

        return presentation


class _Entry(object):
    def __init__(self, presentation, canonical_location, origin_canonical_location):
        self.presentation = presentation
        self.canonical_location = canonical_location
        self.origin_canonical_location = origin_canonical_location
        self.merged = False

    def get_imports(self, entries):
        imports = []

        def has_import(entry):
            for i in imports:
                if i.canonical_location == entry.canonical_location:
                    return True
            return False

        for entry in entries:
            if entry.origin_canonical_location == self.canonical_location:
                if not has_import(entry):
                    imports.append(entry)
        return imports

    def merge(self, entries, context):
        # Make sure to only merge each presentation once
        if self.merged:
            return
        self.merged = True
        for entry in entries:
            if entry.presentation == self.presentation:
                entry.merged = True

        for entry in self.get_imports(entries):
            # Make sure import is merged
            entry.merge(entries, context)

            # Validate import
            if hasattr(self.presentation, '_validate_import'):
                # _validate_import will report an issue if invalid
                valid = self.presentation._validate_import(context, entry.presentation)
            else:
                valid = True

            # Merge import
            if valid and hasattr(self.presentation, '_merge_import'):
                self.presentation._merge_import(entry.presentation)

    def cache(self):
        if not self.merged:
            raise RuntimeError(u'Only merged presentations can be cached: {0}'
                               .format(self.canonical_location))
        PRESENTATION_CACHE[self.canonical_location] = self.presentation


class _Skip(Exception):
    pass
