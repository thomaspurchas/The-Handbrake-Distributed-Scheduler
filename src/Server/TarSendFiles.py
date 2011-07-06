'''
Created on 6 Jul 2011

@author: Thomas Purchas
'''
from twisted.internet.protocol import ServerFactory, Protocol
from tartransfer import sender, client

class Protocol(Protocol):

    def connectionMade(self):

        self.factory.service.Start(self.transport)

class common(object):
    '''
    This has all the common file sending code, like setting up.
    '''
    def __init__(self, Folder):
        '''
        Here we will grab the folder we are going to send and get ready to go.
        '''

        self.folder = Folder

        # Now set up the sending factory.
        self.factory = ServerFactory()
        self.factory.service = self
        self.factory.protocol = Protocol()

        port = reactor.listenTCP(0, self.factory, interface='')

        self.listen = port
        self.port = port.getHost().port
        self.host = port.getHost().host

    def GetInfo(self):

        return (self.port, self.host)

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

        self.port.stopListening()


class FileReceiver(common):
    '''
    This uses the tartransfer library to get files.
    '''
    def Start(self, transport):

        receiver = client.Client(self.folder)

        receiver.registerProducer(transport, True)
