import unittest
import json

from puppetry import RemoteServer, ThreadedRemoteServer, RemoteClient

class EchoClass(object):

    def __init__(self, name=''):
        self.name = name

    def hello(self, name=None):
        if name:
            return 'Hello ' + name
        return 'Hello ' + self.name

    def echo(self, value):
        return value


class JsonSerializer:

    def loads(self, data):
        return json.loads(data.decode())

    def dumps(self, data):
        return json.dumps(data).encode()


class TestEchoClass(unittest.TestCase):

    def test_echo_class_threaded(self):
        server = ThreadedRemoteServer(('localhost', 0), obj=EchoClass('puppetry'))
        addr = server.server.server_address
        server.start()

        client = RemoteClient(addr)
        self.assertEqual(client.name, 'puppetry')
        self.assertEqual(client.echo(value='Test'), 'Test')
        self.assertEqual(client.hello(), 'Hello puppetry')
        self.assertEqual(client.hello(name='Spam'), 'Hello Spam')


    def test_echo_class_threaded_json(self):
        server = ThreadedRemoteServer(('localhost', 0), serializer=JsonSerializer(), obj=EchoClass('puppetry'))
        addr = server.server.server_address
        server.start()

        client = RemoteClient(addr, serializer=JsonSerializer(), cls=EchoClass)
        self.assertEqual(client.name, 'puppetry')
        self.assertEqual(client.echo(value='Test'), 'Test')
        self.assertEqual(client.hello(), 'Hello puppetry')
        self.assertEqual(client.hello(name='Spam'), 'Hello Spam')


    def test_echo_class_server(self):
        server = RemoteServer(('localhost', 0), obj=EchoClass('puppetry'))

        self.assertEqual(server.obj.name, 'puppetry')
        self.assertEqual(server.obj.echo('Test'), 'Test')
        self.assertEqual(server.obj.hello(), 'Hello puppetry')
        self.assertEqual(server.obj.hello('Spam'), 'Hello Spam')


if __name__ == '__main__':
    unittest.main()
