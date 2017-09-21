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

from threading import Lock

from ...utils.threading import (BlockingExecutor, FixedThreadPoolExecutor)
from ...utils.formatting import (json_dumps, yaml_dumps)
from ..loading import UriLocation
from ..presentation import PresenterNotFoundError
from .consumer import Consumer


PRESENTATION_CACHE = {}
CANONICAL_LOCATION_CACHE = {}


class Read(Consumer):
    """
    Reads the presentation, handling imports recursively.

    It works by consuming a data source via appropriate :class:`~aria.parser.loading.Loader`,
    :class:`~aria.parser.reading.Reader`, and :class:`~aria.parser.presentation.Presenter`
    instances.

    It supports agnostic raw data composition for presenters that have
    ``_get_import_locations`` and ``_merge_import``.

    To improve performance, loaders are called asynchronously on separate threads.

    Note that parsing may internally trigger more than one loading/reading/presentation
    cycle, for example if the agnostic raw data has dependencies that must also be parsed.
    """

    def __init__(self, context):
        super(Read, self).__init__(context)
        self._locations = set() # for keeping track of locations already read
        self._locations_lock = Lock()

    def consume(self):
        location = self.context.presentation.location

        if location is None:
            self.context.validation.report('Presentation consumer: missing location')
            return

        presenter = None
        imported_presentations = []

        if self.context.presentation.threads == 1:
            # BlockingExecutor is much faster for the single-threaded case
            executor = BlockingExecutor(print_exceptions=self.context.presentation.print_exceptions)
        else:
            executor = FixedThreadPoolExecutor(size=self.context.presentation.threads,
                                               timeout=self.context.presentation.timeout,
                                               print_exceptions=self.context.presentation \
                                               .print_exceptions)

        try:
            presenter, canonical_location = self._present(location, None, None, executor)
            executor.drain()

            # Handle exceptions
            for e in executor.exceptions:
                self._handle_exception(e)

            imported_presentations = executor.returns
        finally:
            executor.close()

        # Merge imports
        for imported_presentation, _ in imported_presentations:
            okay = True
            if hasattr(presenter, '_validate_import'):
                # _validate_import will report an issue if invalid
                okay = presenter._validate_import(self.context, imported_presentation)
            if okay and hasattr(presenter, '_merge_import'):
                presenter._merge_import(imported_presentation)

                # Make sure merged presenter is not in cache
                if canonical_location is not None:
                    try:
                        del PRESENTATION_CACHE[canonical_location]
                    except KeyError:
                        pass

        if canonical_location is not None:
            self.context.presentation.location = canonical_location
        self.context.presentation.presenter = presenter

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
        if isinstance(e, _AlreadyPresentedException):
            return
        super(Read, self)._handle_exception(e)

    def _present(self, location, origin_location, default_presenter_class, executor):
        # Link the context to this thread
        self.context.set_thread_local()

        presentation = None
        cache = False

        # Canonicalize the location
        if self.context.reading.reader is None:
            loader, canonical_location = self._create_loader(location, origin_location)
            if self.context.presentation.cache:
                cache = True
        else:
            # If a reader is specified in the context we skip loading
            loader = None
            canonical_location = location

        # Make sure we didn't already present this location
        self._verify_not_already_presented(canonical_location)

        # Is the presentation in the cache?
        if cache:
            try:
                presentation = PRESENTATION_CACHE[canonical_location]
            except KeyError:
                pass

        if presentation is None:
            # Create new presentation
            presentation = self._create_presentation(canonical_location, loader,
                                                     default_presenter_class)

            # Cache
            if cache:
                PRESENTATION_CACHE[canonical_location] = presentation

        # Submit imports to executor
        if hasattr(presentation, '_get_import_locations'):
            import_locations = presentation._get_import_locations(self.context)
            if import_locations:
                for import_location in import_locations:
                    # Our imports will default to using our presenter class and use our canonical
                    # location as their origin location
                    import_location = UriLocation(import_location)
                    executor.submit(self._present, import_location, canonical_location,
                                    presentation.__class__, executor)

        return presentation, canonical_location

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

    def _verify_not_already_presented(self, canonical_location):
        with self._locations_lock:
            if canonical_location in self._locations:
                raise _AlreadyPresentedException(u'already presented: {0}'
                                                 .format(canonical_location))
            self._locations.add(canonical_location)


class _AlreadyPresentedException(Exception):
    pass
