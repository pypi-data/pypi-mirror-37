from io import BytesIO

try:
    import httplib
except ImportError:
    import http.client as httplib


orig_connection = httplib.HTTPConnection

from contextlib import contextmanager

import ssl
from array import array

from warcio.utils import to_native_str, BUFF_SIZE

from tempfile import SpooledTemporaryFile

from time import sleep


# ============================================================================
class RecordingStream(object):
    def __init__(self, fp, recorder):
        self.fp = fp
        self.recorder = recorder

        #if hasattr(self.fp, 'unread'):
        #    self.unread = self.fp.unread

        #if hasattr(self.fp, 'tell'):
        #    self.tell = self.fp.tell

    def read(self, amt=None):
        print('called read')
        buff = self.fp.read(amt)
        self.recorder.write_response(buff)
        return buff

    def readline(self, maxlen=None):
        print('called readline')
        line = self.fp.readline(maxlen)
        self.recorder.write_response(line)
        return line

    def readinto(self, buff):
        print('called readinto')
        res = self.fp.readinto(buff)
        self.recorder.write_response(buff)
        return res

    def close(self):
        print('called close')
        try:
            self.recorder.done()
        except Exception as e:
            import traceback
            traceback.print_exc()

        return self.fp.close()


# ============================================================================
class RecordingHTTPResponse(httplib.HTTPResponse):
    def __init__(self, recorder, *args, **kwargs):
        httplib.HTTPResponse.__init__(self, *args, **kwargs)
        self.fp = RecordingStream(self.fp, recorder)


# ============================================================================
class RecordingHTTPConnection(httplib.HTTPConnection):
    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        orig_connection.__init__(self, *args, **kwargs)
        self.recorder = self.global_recorder_maker

        def make_recording_response(*args, **kwargs):
            return RecordingHTTPResponse(self.recorder, *args, **kwargs)

        self.response_class = make_recording_response

    def send(self, data):
        if not self.recorder:
            orig_connection.send(self, data)
            return

        # if sending request body as stream
        if hasattr(data, 'read') and not isinstance(data, array):
            while True:
                buff = data.read(self.BUFF_SIZE)
                if not buff:
                    break

                orig_connection.send(self, buff)
                self.recorder.write_request(buff)
        else:
            orig_connection.send(self, data)
            self.recorder.write_request(data)


    def _get_url(self, data):
        try:
            buff = BytesIO(data)
            line = to_native_str(buff.readline(), 'latin-1')

            path = line.split(' ', 2)[1]
            host = self.host
            port = self.port
            scheme = 'https' if isinstance(self.sock, ssl.SSLSocket) else 'http'

            url = scheme + '://' + host
            if (scheme == 'https' and port != '443') and (scheme == 'http' and port != '80'):
                url += ':' + port

            url += path
        except Exception as e:
            raise

        return url


    def request(self, *args, **kwargs):
        print(args, kwargs)
        #if self.recorder:
        #    self.recorder.start_request(self)

        res = orig_connection.request(self, *args, **kwargs)

        #if self.recorder:
        #    self.recorder.finish_request(self.sock)

        return res


# ============================================================================
class RequestRecorder(object):
    def __init__(self):
        self.request = self._create_buffer()
        self.response = self._create_buffer()

    def _create_buffer(self):
        return SpooledTemporaryFile(BUFF_SIZE)

    def write_request(self, buff):
        self.request.write(buff)

    def write_response(self, buff):
        self.response.write(buff)

    def done(self):
        self.request.seek(0)
        print(to_native_str(self.request.read(), 'latin-1'))
        print('')
        self.response.seek(0)
        print(to_native_str(self.response.read(), 'latin-1'))
        print('')
        self.request.close()
        self.response.close()


# ============================================================================
httplib.HTTPConnection = RecordingHTTPConnection
# ============================================================================

@contextmanager
def record_requests(recorder_maker=None):
    if not recorder_maker:
        recorder_maker = RequestRecorder()

    RecordingHTTPConnection.global_recorder_maker = recorder_maker
    yield
    RecordingHTTPConnection.global_recorder_maker = None

@contextmanager
def orig_requests():
    httplib.HTTPConnection = orig_connection
    yield
    httplib.HTTPConnection = RecordingHTTPConnection


