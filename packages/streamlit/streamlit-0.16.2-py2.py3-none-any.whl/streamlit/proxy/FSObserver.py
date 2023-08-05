# -*- coding: future_fstrings -*-

"""A class that watches the file system"""

# Python 2/3 compatibility
from __future__ import print_function, division, unicode_literals, absolute_import
from streamlit.compatibility import setup_2_3_shims
setup_2_3_shims(globals())

import os
import hashlib

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from streamlit.logger import get_logger
from streamlit.util import get_local_id
LOGGER = get_logger()


class FSObserver(object):
    """A file system observer."""

    @staticmethod
    def get_key(connection):
        return (
            connection.cwd,
            connection.command_line[0],
            connection.command_line[1])

    def __init__(self, connection, callback):
        """Constructor.

        Parameters
        ----------
        connection : ProxyConnection
            The connection that is asking for an observer to be created.
        callback: function(FSObserver, FileSystemEvent)
            The function that should get called when something changes in
            path_to_observe. This function will be called on the observer
            thread, which is created by the watchdog module.
        """
        self.key = FSObserver.get_key(connection)
        LOGGER.info(f'Will observe file system for: {self.key}')

        self._observer = None
        self._callback = callback
        self._is_closed = False

        self.command_line = connection.command_line
        self.cwd = connection.cwd

        self._initialize_observer(connection.source_file_path)

        # Set of clients who are interested in this observer being up.  When
        # this is empty and deregister_consumer() is called, the observer stops
        # watching for filesystem updates.
        self._consumers = set()

    def _initialize_observer(self, source_file_path):
        """Initialize the filesystem observer.

        Parameters
        ----------
        source_file_path : str
            Full path of the file that initiated the report.

        """
        path_to_observe = os.path.dirname(source_file_path)

        fsev_handler = FSEventHandler(
            fn_to_run=self._on_event,
            source_file_path=source_file_path,
        )

        observer = Observer()
        observer.schedule(fsev_handler, path_to_observe, recursive=False)

        try:
            observer.start()
            LOGGER.info(f'Observing file system at {path_to_observe}')
        except OSError as e:
            observer = None
            LOGGER.error(f'Could not start file system observer: {e}')

        return observer

    def _on_event(self, event):
        """Function that gets called when filesystem changes are detected.

        This simply calls the callback function passed during construction.

        Parameters
        ----------
        event : FileSystemEvent
        """
        if self._is_closed:
            LOGGER.info(f'Will not rerun source script.')
        else:
            LOGGER.info(f'Rerunning source script.')
            self._callback(self, event)

    def register_consumer(self, key):
        """Tell observer that it's in use by consumer identified by key.

        While at least one consumer is interested in this observer, it will not
        be disposed of.

        Parameters
        ----------
        key : any
            A unique identifier of the consumer that is interested in this
            observer.
        """
        self._consumers.add(key)

    def deregister_consumer(self, key):
        """Tell observer that it's no longer useful for a given consumer.

        When no more consumers are interested in this observer, it will be
        disposed of.

        Parameters
        ----------
        key : any
            A unique identifier of the consumer that is interested in this
            observer.
        """
        if key in self._consumers:
            self._consumers.remove(key)

        LOGGER.info(f'Deregistered consumers. Now have {len(self._consumers)}')

        if len(self._consumers) == 0:
            self._close()

    def is_closed(self):
        """Return whether this observer is "closed" (i.e. no longer observing).

        Returns
        -------
        boolean
            True if closed.
        """
        return self._is_closed

    def _close(self):
        """Stops observing the file system."""
        LOGGER.info(f'Closing file system observer for {self.key}')
        self._is_closed = True

        if self._observer is not None:
            self._observer.stop()

            # Wait til thread terminates.
            self._observer.join(timeout=5)


class FSEventHandler(PatternMatchingEventHandler):
    """Calls a function whenever a watched file changes."""

    def __init__(self, fn_to_run, source_file_path):
        """Constructor.

        Parameters
        ----------
        fn_to_run : function
            The function to call whenever a watched file changes. Takes the
            FileSystemEvent as a parameter.

        More information at https://pythonhosted.org/watchdog/api.html#watchdog.events.PatternMatchingEventHandler
        """
        super(FSEventHandler, self).__init__(patterns=[source_file_path])
        self._fn_to_run = fn_to_run
        self._source_file_path = source_file_path
        self._prev_md5 = _calc_md5(source_file_path)

    def on_any_event(self, event):
        """Catch-all event handler.

        See https://pythonhosted.org/watchdog/api.html#watchdog.events.FileSystemEventHandler.on_any_event

        Parameters
        ----------
        event : FileSystemEvent
            The event object representing the file system event.

        """
        new_md5 = _calc_md5(self._source_file_path)
        if new_md5 != self._prev_md5:
            LOGGER.info(f'File MD5 changed.')
            self._prev_md5 = new_md5
            self._fn_to_run(event)
        else:
            LOGGER.info(f'File MD5 did not change.')


def _calc_md5(file_path):
    """Calculate the MD5 checksum of the given file.

    Parameters
    ----------
    file_path : str
        The path of the file to check.

    Returns
    -------
    str
        The MD5 checksum.
    """
    md5 = hashlib.md5()
    md5.update(open(file_path).read().encode('utf-8'))
    return md5.digest()
