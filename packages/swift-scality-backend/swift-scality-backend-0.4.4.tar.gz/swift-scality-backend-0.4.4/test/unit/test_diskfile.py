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

"""Tests for swift_scality_backend.diskfile"""

import hashlib
import httplib
import logging
import StringIO
import time
import unittest

import mock
import swift.common.exceptions
import swift.common.utils

from swift_scality_backend.diskfile import DiskFileWriter, \
    DiskFileReader, DiskFile, DiskFileManager
from scality_sproxyd_client.exceptions import SproxydHTTPException
from swift_scality_backend.http_utils import ClientCollection
from scality_sproxyd_client.sproxyd_client import SproxydClient
from . import utils
from .utils import make_client_collection


NEW_SPLICE = 'new_splice'
OLD_SPLICE = 'old_splice'
NO_SPLICE_AT_ALL = 'no_splice_at_all'
try:
    import swift.common.splice
    SPLICE = NEW_SPLICE
except ImportError:
    if hasattr(swift.common.utils, 'system_has_splice'):
        SPLICE = OLD_SPLICE
    else:
        SPLICE = NO_SPLICE_AT_ALL


class FakeHTTPResp(httplib.HTTPResponse):

    def __init__(self, status=200):
        self.status = status
        self.reason = 'because'

    def read(self):
        return 'My mock msg'


class FakeHTTPConn(mock.Mock):

    def __init__(self, *args, **kwargs):
        super(FakeHTTPConn, self).__init__(*args, **kwargs)
        self.resp_status = kwargs.get('resp_status', 200)
        self._buffer = StringIO.StringIO()

    def getresponse(self):
        return FakeHTTPResp(self.resp_status)

    def send(self, data):
        self._buffer.write(data)


class TestDiskFileManager(unittest.TestCase):
    """Tests for swift_scality_backend.diskfile.DiskFileManager"""

    def test_init_with_default_splice(self):
        dfm = DiskFileManager({}, mock.Mock())
        self.assertFalse(dfm.use_splice)

    def test_init_with_splice_no(self):
        dfm = DiskFileManager({'splice': 'no'}, mock.Mock())
        self.assertFalse(dfm.use_splice)

    def _test_init_splice_unavailable(self):
        dfm = DiskFileManager({'splice': 'no'}, mock.Mock())
        self.assertFalse(dfm.use_splice, "Splice not wanted by conf and not " +
                         "available from system: use_splice should be False")

        mock_logger = mock.Mock()
        dfm = DiskFileManager({'splice': 'yes'}, mock_logger)
        self.assertFalse(dfm.use_splice, "Splice wanted by conf but not " +
                         "available from system: use_splice should be False")
        self.assertTrue(mock_logger.warn.called)

    def _test_init_splice_available(self):
        dfm = DiskFileManager({'splice': 'yes'}, mock.Mock())
        self.assertTrue(dfm.use_splice, "Splice wanted by conf and " +
                        "available from system: use_splice should be True")

        dfm = DiskFileManager({'splice': 'no'}, mock.Mock())
        self.assertFalse(dfm.use_splice, "Splice not wanted by conf though " +
                         "available from system: use_splice should be False")

    @utils.skipIf(SPLICE != NEW_SPLICE, 'Need new `splice` support')
    @mock.patch('swift.common.splice.splice')
    def test_init_new_splice_unavailable(self, mock_splice):
        type(mock_splice).available = mock.PropertyMock(return_value=False)
        self._test_init_splice_unavailable()

    @utils.skipIf(SPLICE != NEW_SPLICE, 'Need new `splice` support')
    @mock.patch('swift.common.splice.splice')
    def test_init_new_splice_is_available(self, mock_splice):
        type(mock_splice).available = mock.PropertyMock(return_value=True)
        self._test_init_splice_available()

    @utils.skipIf(SPLICE != OLD_SPLICE, 'Need old `splice` support')
    @mock.patch.object(swift.common.utils, 'system_has_splice',
                       return_value=True)
    def test_init_old_splice_is_available(self, mock_splice):
        self._test_init_splice_available()

    @utils.skipIf(SPLICE != OLD_SPLICE, 'Need old `splice` support')
    @mock.patch.object(swift.common.utils, 'system_has_splice',
                       return_value=False)
    def test_init_old_splice_unavailable(self, mock_splice):
        self._test_init_splice_unavailable()

    @utils.skipIf(SPLICE != NO_SPLICE_AT_ALL, 'This Swift knows `splice`')
    def test_init_no_splice_at_all(self):
        self._test_init_splice_unavailable()

    def test_get_diskfile(self):
        client_collection = make_client_collection()
        dfm = DiskFileManager({}, mock.Mock())

        diskfile = dfm.get_diskfile(client_collection, 'a', 'c', 'o')
        self.assertTrue(isinstance(diskfile, DiskFile))


class TestDiskFileWriter(unittest.TestCase):
    """Tests for swift_scality_backend.diskfile.DiskFileWriter"""

    @mock.patch('scality_sproxyd_client.sproxyd_client.SproxydClient.get_http_conn_for_put',
                return_value=(None, None))
    def test_init(self, mock_http):
        client_collection = make_client_collection()
        # Note the white space, to test proper URL encoding
        DiskFileWriter(client_collection, 'ob j', logger=logging.root)

        expected_header = {'transfer-encoding': 'chunked'}
        mock_http.assert_called_once_with('ob j', expected_header)

    @mock.patch('scality_sproxyd_client.sproxyd_client.SproxydClient.get_http_conn_for_put',
                return_value=(FakeHTTPConn(resp_status=404), None))
    def test_put_with_404_response(self, mock_http):
        client_collection = make_client_collection()
        dfw = DiskFileWriter(client_collection, 'obj', logger=logging.root)

        fake_http_conn = mock_http.return_value[0]
        msg = r'.*404 / %s.*' % fake_http_conn.getresponse().read()
        utils.assertRaisesRegexp(SproxydHTTPException, msg, dfw.put, {})

        fake_http_conn.close.assert_called_once_with()

    @mock.patch('scality_sproxyd_client.sproxyd_client.SproxydClient.get_http_conn_for_put',
                return_value=(FakeHTTPConn(), mock.Mock()))
    @mock.patch('scality_sproxyd_client.sproxyd_client.SproxydClient.put_meta')
    def test_put_with_200_response(self, mock_put_meta, mock_http):
        client_collection = make_client_collection()
        dfw = DiskFileWriter(client_collection, 'obj', logger=logging.root)

        dfw.put({'meta1': 'val'})

        fake_http_conn = mock_http.return_value[0]
        self.assertEqual('0\r\n\r\n', fake_http_conn._buffer.getvalue())

        mock_release_conn = mock_http.return_value[1]
        mock_release_conn.assert_called_once_with()

        mock_put_meta.assert_called_with('obj', {
            'df': {'meta1': 'val'},
            'meta1': 'val',
            'mf': {},
            'ETag': 'd41d8cd98f00b204e9800998ecf8427e',
            'name': 'obj'
        })

    @mock.patch('scality_sproxyd_client.sproxyd_client.SproxydClient.get_http_conn_for_put',
                return_value=(FakeHTTPConn(), mock.Mock()))
    def test_write_no_data(self, mock_http):
        dfw = DiskFileWriter(make_client_collection(), 'obj',
                             logger=logging.root)

        written = dfw.write("")

        self.assertEqual(0, written)
        fake_http_conn = mock_http.return_value[0]
        self.assertEqual('0\r\n\r\n', fake_http_conn._buffer.getvalue())

    @mock.patch('scality_sproxyd_client.sproxyd_client.SproxydClient.get_http_conn_for_put',
                return_value=(FakeHTTPConn(), mock.Mock()))
    def test_write_with_data(self, mock_http):
        dfw = DiskFileWriter(make_client_collection(), 'obj',
                             logger=logging.root)

        data = "a" * 4096
        written = dfw.write(data)

        self.assertEqual(len(data), written)
        fake_http_conn = mock_http.return_value[0]
        self.assertEqual('%x\r\n%s\r\n' % (len(data), data),
                         fake_http_conn._buffer.getvalue())


class TestDiskFileReader(unittest.TestCase):

    def test_app_iter_ranges_with_no_ranges(self):
        dfr = DiskFileReader(make_client_collection(), 'obj', False,
                             logger=logging.root)

        gen = dfr.app_iter_ranges([], mock.sentinel.arg1,
                                  mock.sentinel.arg2, mock.sentinel.arg3)
        self.assertEqual('', gen.next())
        self.assertRaises(StopIteration, gen.next)

    @mock.patch('swift.common.swob.multi_range_iterator')
    def test_app_iter_ranges(self, mock_mri):
        mock_mri.return_value = iter(['data'])
        dfr = DiskFileReader(make_client_collection(), 'obj', False,
                             logger=logging.root)

        gen = dfr.app_iter_ranges([(1, 100)], mock.sentinel.arg1,
                                  mock.sentinel.arg2, mock.sentinel.arg3)

        self.assertEqual('data', gen.next())
        self.assertRaises(StopIteration, gen.next)
        mock_mri.assert_called_once_with([(1, 100)], mock.sentinel.arg1,
                                         mock.sentinel.arg2, mock.sentinel.arg3,
                                         dfr.app_iter_range)


class TestDiskFile(unittest.TestCase):
    """Tests for swift_scality_backend.diskfile.DiskFile"""

    @staticmethod
    def hash_str(strings):
        "Get a SHA1 hex hash of the iterable of `str` passed as arguments"

        sha1 = hashlib.sha1()
        for string in strings:
            sha1.update(string)
        return sha1.hexdigest()

    def test_init_quotes_object_path(self):
        acc, cont, obj = 'a', '@/', '/ob/j'

        sproxyd_client = SproxydClient(['http://host:81/path/'], logger=mock.Mock())
        df = DiskFile(sproxyd_client, acc, cont, obj,
                      use_splice=False, logger=logging.root)
        self.assertEqual(self.hash_str([acc, cont, obj]), df._name)

    @mock.patch('scality_sproxyd_client.sproxyd_client.SproxydClient.get_meta',
                return_value=None)
    def test_open_when_no_metadata(self, mock_get_meta):
        acc, cont, obj = 'a', 'c', 'o'

        client_collection = make_client_collection()
        df = DiskFile(client_collection, acc, cont, obj, use_splice=False,
                      logger=logging.root)

        self.assertRaises(swift.common.exceptions.DiskFileDeleted, df.open)
        mock_get_meta.assert_called_once_with(self.hash_str([acc, cont, obj]))

    @mock.patch('scality_sproxyd_client.sproxyd_client.SproxydClient.get_meta',
                return_value={'name': 'o'})
    def test_open(self, mock_get_meta):
        client_collection = make_client_collection()
        df = DiskFile(client_collection, 'a', 'c', 'o', use_splice=False,
                      logger=logging.root)

        df.open()

        self.assertEqual({'name': 'o', 'mf': {}, 'df': {'name': 'o'}}, df._metadata)

    @mock.patch('scality_sproxyd_client.sproxyd_client.SproxydClient.get_meta')
    def test_open_expired_file(self, mock_get_meta):
        acc, cont, obj = 'a', 'c', 'o'
        mock_get_meta.return_value = {'X-Delete-At': time.time() - 10}

        client_collection = make_client_collection()
        df = DiskFile(client_collection, acc, cont, obj, use_splice=False,
                      logger=logging.root)
        self.assertRaises(swift.common.exceptions.DiskFileExpired, df.open)
        mock_get_meta.assert_called_once_with(self.hash_str([acc, cont, obj]))

    def test_get_metadata_when_diskfile_not_open(self):
        client_collection = make_client_collection()
        df = DiskFile(client_collection, 'a', 'c', 'o', use_splice=False,
                      logger=logging.root)

        self.assertRaises(swift.common.exceptions.DiskFileNotOpen,
                          df.get_metadata)

    @mock.patch('scality_sproxyd_client.sproxyd_client.SproxydClient.get_meta',
                return_value={'name': 'o'})
    def test_read_metadata(self, mock_get_meta):
        client_collection = make_client_collection()
        df = DiskFile(client_collection, 'a', 'c', 'o', use_splice=False,
                      logger=logging.root)

        metadata = df.read_metadata()

        self.assertEqual({'name': 'o'}, metadata)

    def test_reader(self):
        client_collection = make_client_collection()
        df = DiskFile(client_collection, 'a', 'c', 'o', use_splice=False,
                      logger=logging.root)

        reader = df.reader()
        self.assertTrue(isinstance(reader, DiskFileReader))

    @mock.patch('scality_sproxyd_client.sproxyd_client.SproxydClient.get_http_conn_for_put',
                return_value=(FakeHTTPConn(), mock.Mock()))
    def test_create(self, mock_http):
        client_collection = make_client_collection()
        df = DiskFile(client_collection, 'a', 'c', 'o', use_splice=False,
                      logger=logging.root)

        with df.create() as writer:
            self.assertTrue(isinstance(writer, DiskFileWriter))

    @mock.patch('scality_sproxyd_client.sproxyd_client.SproxydClient.put_meta')
    def test_write_metadata(self, mock_put_meta):
        acc, cont, obj = 'a', 'c', 'o'

        client_collection = make_client_collection()
        df = DiskFile(client_collection, acc, cont, obj, use_splice=False,
                      logger=logging.root)

        df.write_metadata({'k': 'v'})

        mock_put_meta.assert_called_once_with(self.hash_str([acc, cont, obj]), {
            'df': {'name': 'ae541120074a053234ef14e1b050ee3a7433099c'},
            'k': 'v',
            'mf': {'k': 'v'}
        })

    @mock.patch('scality_sproxyd_client.sproxyd_client.SproxydClient.del_object')
    def test_delete(self, mock_del_object):
        acc, cont, obj = 'a', 'c', 'o'

        client_collection = make_client_collection()
        df = DiskFile(client_collection, acc, cont, obj, use_splice=False,
                      logger=logging.root)

        df.delete("ignored")

        mock_del_object.assert_called_once_with(self.hash_str([acc, cont, obj]))

    @utils.skipIf(not hasattr(swift.common.utils, 'Timestamp'), 'Swift2+ only')
    def test_timestamps_when_no_metadata(self):
        client_collection = make_client_collection()
        df = DiskFile(client_collection, 'a', 'c', 'o', use_splice=False,
                      logger=logging.root)

        # assertRaises expects a `callable`, but `timestamp` is a property
        # We could use the `with self.assertRaises(exc):` form but that's
        # Python 2.7+ only
        self.assertRaises(swift.common.exceptions.DiskFileNotOpen,
                          lambda: df.timestamp)
        self.assertRaises(swift.common.exceptions.DiskFileNotOpen,
                          lambda: df.data_timestamp)

    @utils.skipIf(not hasattr(swift.common.utils, 'Timestamp'), 'Swift2+ only')
    @mock.patch('swift.common.utils.Timestamp')
    def test_timestamp(self, mock_timestamp):
        client_collection = make_client_collection()
        df = DiskFile(client_collection, 'a', 'c', 'o', use_splice=False,
                      logger=logging.root)

        df._metadata = mock.Mock()
        df.timestamp

        df._metadata.get.assert_called_once_with('X-Timestamp')
        mock_timestamp.assert_called_once_with(df._metadata.get())


class TestClientCollection(unittest.TestCase):
    '''Tests for `swift_scality_backend.diskfile.ClientCollection`'''

    def test_constructor(self):
        def make_iter():
            cell = [False]

            def iter():
                yield ()
                cell[0] = True
                yield ()

            return cell, iter()

        read_set_cell, read_set = make_iter()
        write_set_cell, write_set = make_iter()

        ClientCollection(read_set, write_set)

        self.assertTrue(read_set_cell[0])
        self.assertTrue(write_set_cell[0])

    def test_hash(self):
        col = ClientCollection([None, None], [None])
        hash(col)
