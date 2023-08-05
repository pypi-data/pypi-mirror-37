import json

import time


# ==========
# EXCEPTIONS
# ==========

class JRPCInvalidMessage(Exception):
    pass


class JRPCInvalidResponseException(JRPCInvalidMessage):
    pass


class JRPCInvalidRequestException(JRPCInvalidMessage):
    pass


# ===============
# JSON RPC ERRORS
# ===============

class JRPCError(object):
    def __init__(self, *, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        if not isinstance(value, int):
            raise TypeError('code must be an integer')
        self._code = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if not isinstance(value, str):
            raise TypeError('message must be a string')
        self._message = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def json(self):
        return json.dumps(dict(self))

    def __getitem__(self, key):
        return dict(zip(['code', 'message', 'data'],
                        [self.code, self.message, self.data]))[key]

    def keys(self):
        keys = ['code', 'message']
        if self.data is not None:
            keys.append('data')
        return keys

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if isinstance(other, JRPCError):
            return (self.code == other.code and
                    self.message == other.message and
                    self.data == other.data)
        if isinstance(other, dict):
            return dict(self) == other
        return False

    def __str__(self):
        return self.json


JRPCParseError = dict(code=-32700, message='Parse error')
JRPCInvalidRequest = dict(code=-32600, message='Invalid request')
JRPCMethodNotFound = dict(code=-32601, message='Method not found')
JRPCInvalidParams = dict(code=-32602, message='Invalid params')
JRPCInternalError = dict(code=-32603, message='Internal error')
JRPCServerError = dict(code=-32000, message='Server error')


# =================
# JSON RPC MESSAGES
# =================

class JRPCMessage(object):
    def __init__(self):
        self._data = dict(jsonrpc='2.0')

    @property
    def id(self):
        return self._data.get('id')

    @id.setter
    def id(self, value):
        if value is None or isinstance(value, (str, int)):
            self._data['id'] = value
        else:
            raise TypeError('id must be an integer or a string')

    @id.deleter
    def id(self):
        try:
            self._data['id']
        except KeyError:
            pass

    @property
    def json(self):
        return json.dumps(self._data)

    @classmethod
    def from_json(cls, js):
        data = json.loads(js)
        return cls.from_data(data)

    @classmethod
    def from_data(cls, data):
        if not isinstance(data, dict):
            raise TypeError('data must be a dictionary')
        if 'jsonrpc' not in data:
            raise JRPCInvalidMessage('missing "jsonrpc" key')
        if data['jsonrpc'] != '2.0':
            raise JRPCInvalidMessage('invalid JSON RPC version')
        if 'method' in data:
            try:
                return JRPCRequest.from_data(data)
            except Exception as e:
                raise JRPCInvalidRequestException from e
        elif 'result' in data or 'error' in data:
            try:
                return JRPCResponse.from_data(data)
            except Exception as e:
                raise JRPCInvalidResponseException from e
        else:
            raise JRPCInvalidMessage('missing specific keys ("method", "result" or "error"')

    def __str__(self):
        return self.json


class JRPCRequest(JRPCMessage):
    REQUIRED_FIELDS = {'jsonrpc', 'method'}
    POSSIBLE_FIELDS = REQUIRED_FIELDS | {'id', 'params'}

    def __init__(self, method: str, params=None, id=None, is_notification=False):
        super().__init__()
        if not is_notification:
            if id is None:
                self._data['id'] = '{:.6f}'.format(time.time())
            else:
                self.id = id
        self.method = method
        if params is not None:
            self.params = params

    @property
    def method(self):
        return self._data['method']

    @method.setter
    def method(self, value):
        if not isinstance(value, str):
            raise TypeError('method must be a string')
        self._data['method'] = value

    @property
    def params(self):
        return self._data.get('params')

    @params.setter
    def params(self, value):
        if not isinstance(value, (list, dict, tuple)):
            raise TypeError('params must be a list, dictionary or a tuple')
        self._data['params'] = value

    @params.deleter
    def params(self):
        try:
            del self._data['params']
        except KeyError:
            pass

    @property
    def is_notification(self):
        return 'id' not in self._data

    @classmethod
    def from_data(cls, data):
        if not isinstance(data, dict):
            raise TypeError('data must be a dictionary')
        if not cls.REQUIRED_FIELDS <= set(data.keys()) <= cls.POSSIBLE_FIELDS:
            missing = cls.REQUIRED_FIELDS - set(data.keys())
            extra = set(data.keys()) - cls.POSSIBLE_FIELDS
            msg = 'Invalid request. Missing fields: {}, extra fields: {}'
            raise JRPCInvalidRequestException(msg.format(missing, extra))
        if data['jsonrpc'] != '2.0':
            raise JRPCInvalidRequestException('Invalid request. Invalid JSON RPC version')
        return JRPCRequest(data['method'], data.get('params'), data.get('id'), 'id' not in data)


class JRPCResponse(JRPCMessage):
    REQUIRED_FIELDS = {'jsonrpc', 'id'}
    POSSIBLE_FIELDS = REQUIRED_FIELDS | {'result', 'error'}

    def __init__(self, id=None, result=None, error=None):
        super().__init__()
        self.id = id
        self.result = result
        self.error = error

    @property
    def result(self):
        return self._data.get('result')

    @result.setter
    def result(self, value):
        if self.error is not None:
            raise ValueError('result and error are mutually exclusive')
        self._data['result'] = value

    @property
    def error(self):
        return self._data.get('error')

    @error.setter
    def error(self, value):
        if value is None:
            try:
                del self._data['error']
            except KeyError:
                pass
        elif not isinstance(value, (dict, JRPCError)):
            raise TypeError('error must ba a dictionary or JRPCError')
        elif self.result is not None:
            raise ValueError('result and error are mutually exclusive')
        else:
            if isinstance(value, dict):
                JRPCError(**value)
                self._data['error'] = value
            else:
                self._data['error'] = dict(value)
            try:
                del self._data['result']
            except KeyError:
                pass

    @classmethod
    def from_data(cls, data):
        if not isinstance(data, dict):
            raise TypeError('data must be a dictionary')
        if not cls.REQUIRED_FIELDS < set(data.keys()) < cls.POSSIBLE_FIELDS:
            missing = cls.REQUIRED_FIELDS - set(data.keys())
            extra = set(data.keys()) - cls.POSSIBLE_FIELDS
            msg = 'Invalid response. Missing fields: {}, extra fields: {}'
            raise JRPCInvalidResponseException(msg.format(missing, extra))
        if data['jsonrpc'] != '2.0':
            raise JRPCInvalidResponseException('Invalid response. Invalid JSON RPC version')
        if 'error' in data and data['error'] is None:
            raise JRPCInvalidResponseException('Invalid response. "error" cannot be None')
        return JRPCResponse(data['id'], data.get('result'), data.get('error'))
