# Copyright (c) 2014, 2015 Scality
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A collection of functions that helps running unit tests"""

import functools
import re
import unittest

import eventlet
import mock
import nose.plugins.skip

from swift_scality_backend.http_utils import ClientCollection

from scality_sproxyd_client.sproxyd_client import SproxydClient


def skipIf(condition, reason):
    """
    A `skipIf` decorator.

    Similar to `unittest.skipIf`, for Python 2.6 compatibility.
    """
    def decorator(test_item):
        @functools.wraps(test_item)
        def wrapped(*args, **kwargs):
            if condition:
                raise nose.plugins.skip.SkipTest(reason)
            else:
                return test_item(*args, **kwargs)
        return wrapped
    return decorator


def assertRaisesRegexp(expected_exception, expected_regexp,
                       callable_obj, *args, **kwargs):
    """Asserts that the message in a raised exception matches a regexp."""
    try:
        callable_obj(*args, **kwargs)
    except expected_exception as exc_value:
        if not re.search(expected_regexp, str(exc_value)):
            # We accept both `string` and compiled regex object as 2nd
            # argument to assertRaisesRegexp
            pattern = getattr(expected_regexp, 'pattern', expected_regexp)
            raise unittest.TestCase.failureException(
                '"%s" does not match "%s"' %
                (pattern, str(exc_value)))
    else:
        if hasattr(expected_exception, '__name__'):
            excName = expected_exception.__name__
        else:
            excName = str(expected_exception)
        raise unittest.TestCase.failureException("%s not raised" % excName)


def assertRegexpMatches(text, expected_regexp, msg=None):
    '''Asserts the text matches the regular expression.'''

    if isinstance(expected_regexp, basestring):
        expected_regexp = re.compile(expected_regexp)

    if not expected_regexp.search(text):
        msg = msg or "Regexp didn't match"
        msg = '%s: %r not found in %r' % (msg, expected_regexp.pattern, text)
        raise unittest.TestCase.failureException(msg)


def make_client_collection(endpoints=None, conn_timeout=None,
                           read_timeout=None, logger=None):
    '''Construct an `SproxydClient` instance using default values.'''

    def maybe(default, value):
        return value if value is not None else default

    endpoints = maybe(['http://localhost:81/proxy/chord/'], endpoints)
    conn_timeout = maybe(10.0, conn_timeout)
    read_timeout = maybe(3.0, read_timeout)
    logger = maybe(mock.Mock(), logger)

    client = SproxydClient(
        endpoints=endpoints, conn_timeout=conn_timeout,
        read_timeout=read_timeout, logger=logger)

    return ClientCollection(read_clients=[client], write_clients=[client])


class WSGIServer(object):
    """Start a WSGI Web server."""
    def __init__(self, application):
        self.application = application

    def __enter__(self):
        self._server = eventlet.listen(('127.0.0.1', 0))
        (self.ip, self.port) = self._server.getsockname()
        self._thread = eventlet.spawn(eventlet.wsgi.server, self._server,
                                      self.application)
        return self

    def __exit__(self, exc_ty, exc_val, tb):
        try:
            self._thread.kill()
        finally:
            self._server.close()
