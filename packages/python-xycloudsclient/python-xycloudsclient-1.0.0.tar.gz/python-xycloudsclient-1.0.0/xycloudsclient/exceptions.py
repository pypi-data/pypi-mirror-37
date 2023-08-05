# Copyright 2010 Jacob Kaplan-Moss
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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
HTTP_CODE_BAD_REQ = 400
HTTP_CODE_UNAUTH = 401
HTTP_CODE_NOT_FOUND = 404
HTTP_CODE_INTERNAL_SERVER_ERROR = 500
MSG_SYNC_FAIL = 'sync login failed'
MSG_USER_LOCKED = 'password error too many times, ' \
                  'please wait for %ss and try again.'


class UnsupportedVersion(Exception):
    """Indicates that the user is trying to use an unsupported
    version of the API.
    """
    pass


class XycloudsException(Exception):
    """
    The base exception class for all exceptions this library raises.
    """
    message = 'Unknown Error'

    def __init__(self, code=None, message=None, url=None, method=None, **kwargs):
        self.code = code or self.__class__.http_status
        self.message = message or self.__class__.message % kwargs
        self.url = url
        self.method = method

    def __str__(self):
        self.message = "%s (HTTP %s)" % (self.message, self.code)
        return self.message


class ClientException(XycloudsException):
    """
    The base exception class for all exceptions this library raises.
    """
    http_status = 400
    message = 'Unknown Error'


class BadRequest(ClientException):
    """
    HTTP 400 - Bad request: you sent some malformed data.
    """
    http_status = HTTP_CODE_BAD_REQ
    message = "Bad request"


class InvalidInput(BadRequest):
    """
    HTTP 400 - Invalid Parameters..
    """
    http_status = HTTP_CODE_BAD_REQ
    message = "Invalid input received: %(reason)s"


class ParamsInitError(BadRequest):
    """
    HTTP 400 - Init error.
    """
    http_status = HTTP_CODE_BAD_REQ
    message = "Init error: %(reason)s"


class Unauthorized(ClientException):
    """
    HTTP 401 - Unauthorized: bad credentials.
    """
    http_status = HTTP_CODE_UNAUTH
    message = "Unauthorized"


class NotFound(ClientException):
    """
    HTTP 404 - Not found
    """
    http_status = HTTP_CODE_NOT_FOUND
    message = "Not found"


class ServerException(XycloudsException):
    """
    The base exception class for all exceptions this library raises.
    """
    http_status = 500
    message = 'HTTP Server Error'


class InternalServerError(ServerException):
    """HTTP 500 - Internal Server Error.

    A generic error message, given when no more specific message is suitable.
    """
    http_status = HTTP_CODE_INTERNAL_SERVER_ERROR
    message = "Internal Server Error: %(reason)s"


_error_classes = [BadRequest, Unauthorized, NotFound, InternalServerError]
_code_map = dict((c.http_status, c) for c in _error_classes)


def from_response(code, url=None, method=None, message=None):
    """
    Return an instance of an ClientException or subclass
    based on an requests response.
    """
    try:
        cls = _code_map[code]
    except KeyError:
        if 500 <= code < 600:
            cls = ServerException
        else:
            cls = ClientException

    kwargs = {'code': code, 'method': method, 'url': url, 'message': message}

    return cls(**kwargs)
