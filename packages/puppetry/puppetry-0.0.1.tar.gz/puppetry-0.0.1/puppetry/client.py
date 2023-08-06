import pickle
import socket

def _send(addr, data, serializer):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(addr)
        sock.sendall(serializer.dumps(data))
        return serializer.loads(sock.recv(1024))
    finally:
        sock.close()

def _load_method(addr, serializer):
    cls = _send(addr, {'func': 'cls'}, serializer)
    return [name for name in cls.__dict__]


def _load_variabl(addr, serializer):
    obj = _send(addr, {'func': 'obj'}, serializer)
    return [name for name in obj.__dict__]


class Wrapper(object):

    def __init__(self, addr, method, serializer):
        self.addr = addr
        self.method = method
        self.serializer = serializer

    def __call__(self, **kwargs):
        return _send(self.addr, {'method': self.method, 'kwargs': kwargs}, self.serializer)


class RemoteClient(object):

    def __init__(self, addr, serializer=pickle, load=True, **kwargs):
        self._meta = {'addr': addr, 'method': [], 'variabl': [], 'serializer': serializer}

        cls = kwargs.get('cls')
        if cls:
            self._meta['method'] = [name for name in cls.__dict__]
            obj = cls(**kwargs['kwargs']) if 'kwargs' in kwargs else cls()
            self._meta['variabl'] = [name for name in obj.__dict__]

        elif load:
            self._meta['method'] = _load_method(addr, self._meta['serializer'])
            self._meta['variabl'] = _load_variabl(addr, self._meta['serializer'])


    def __getattr__(self, name):
        if name in self._meta['method']:
            return Wrapper(self._meta['addr'], name, self._meta['serializer'])

        if name in self._meta['variabl']:
            return _send(self._meta['addr'], {'variabl': name}, self._meta['serializer'])


    def __setattr__(self, name, value):
        if name == '_meta':
            super(RemoteClient, self).__setattr__(name, value)
        elif name in self._meta['variabl']:
            _send(self._meta['addr'], {'variabl': name, 'value': value}, self._meta['serializer'])
        else:
            raise Exception('No attribut named {}'.format(name))
