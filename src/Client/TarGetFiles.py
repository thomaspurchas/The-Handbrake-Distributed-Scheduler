'''
Created on 6 Jul 2011

@author: Thomas Purchas
'''

from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import defer, reactor
from tartransfer import sender, client

class Protocol(Protocol):

    def connectionMade(self):

        self.factory.service.Start(self.transport)

    def connectionLost(self, _):

        self.factory.service.finished()

    def dataReceived(self, data):

        self.factory.service.receiver.write(data)

class common(object):
    '''
    This has all the common file getting code, like setting up.
    '''
    def __init__(self, Folder, Port, Host):
        '''
        Here we will grab the folder we are going to put the files, the port,
        the host, and then get ready to go.
        '''

        self.folder = Folder

        # Now set up the sending factory.
        self.factory = ClientFactory()
        self.factory.service = self
        self.factory.protocol = Protocol

        reactor.connectTCP(Host, Port, self.factory)

        self.deferred = defer.Deferred()

    def finished(self):
        '''
        Transfer finished, call the deferreds callback.
        '''
        print 'Got files and finished transfer'
        if self.deferred is not None:
            d, self.deferred = self.deferred, None

            d.callback(None)

class FileSender(common):
    '''
    This uses the tartransfer library to send files.
    '''
    def Start(self, transport):
        '''
        This gets called by the :class:`.Protocol` with the transport.
        '''

        sender = sender.Sender()

        sender.beginTransfer(transport, self.folder)

class FileReceiver(common):
    '''
    This uses the tartransfer library to get files.
    '''
    def Start(self, transport):

        self.receiver = client.Client(self.folder)

        self.receiver.registerProducer(transport, True)
