import socketserver
import threading
import pickle

class PuppetHandler(socketserver.BaseRequestHandler):

    def method(self, data):
        method_to_call = getattr(self.server.obj, data['method'])
        if 'kwargs' in data:
            return method_to_call(**data['kwargs'])
        else:
            return method_to_call()

    def variabl(self, data):
        if 'value' in data:
            return setattr(self.server.obj, data['variabl'], data['value'])
        return getattr(self.server.obj, data['variabl'])

    def func(self, data):
        if data['func'] == 'cls':
            return self.server.obj.__class__

        if data['func'] == 'obj':
            return self.server.obj

    def handle(self):
        serialized = self.request.recv(1024)
        data = self.server.serializer.loads(serialized)

        if 'method' in data:
            result = self.method(data)

        if 'variabl' in data:
            result = self.variabl(data)

        if 'func' in data:
            result = self.func(data)

        self.request.send(self.server.serializer.dumps(result))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class RemoteServer(object):
    server = None

    def __init__(self, addr, serializer=pickle, server_cls=socketserver.TCPServer, handler_cls=PuppetHandler, **kwargs):
        if 'obj' in kwargs:
            obj = kwargs['obj']

        elif 'cls' in kwargs:
            obj = kwargs['cls'](**kwargs.get('kwargs', {}))

        else:
            raise Exception('No object to remote')

        self.setup(addr, server_cls, handler_cls)
        self.server.serializer = serializer
        self.server.obj = obj
        self.running = False

    def __del__(self):
        self.close()

    def __exit__(self):
        self.close()

    def __enter__(self):
        return self

    @property
    def obj(self):
        return self.server.obj

    def close(self):
        if self.server:
            if self.running: self.server.shutdown()
            self.server.server_close()
            self.server = None

    def setup(self, addr, server_cls, handler_cls):
        self.server = server_cls(addr, handler_cls)

    def start(self):
        try:
            self.server.serve_forever()
            self.running = True
        except KeyboardInterrupt:
            print('Exit server')
        except Exception as e:
            raise
        self.running = False


class ThreadedRemoteServer(RemoteServer):

    def __init__(self, addr, serializer=pickle, server_cls=ThreadedTCPServer, handler_cls=PuppetHandler, **kwargs):
        super(ThreadedRemoteServer, self).__init__(addr, serializer, server_cls, handler_cls, **kwargs)


    def setup(self, addr, server_cls, handler_cls):
        self.server = server_cls(addr, handler_cls)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True

    def start(self):
        self.running = True
        self.thread.start()
