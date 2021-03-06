'''
Created on 6 Jul 2011

@author: Thomas Purchas
'''
from twisted.internet.protocol import ServerFactory, Protocol
from twisted.internet import reactor
from tartransfer import sender, client
from os import path

class Protocol(Protocol):

    def connectionMade(self):

        self.factory.service.Start(self.transport)

    def dataReceived(self, data):

        self.factory.service.receiver.write(data)

class common(object):
    '''
    This has all the common file sending code, like setting up.
    '''
    def __init__(self, Folder):
        '''
        Here we will grab the folder we are going to send and get ready to go.
        '''

        self.folder = path.abspath(Folder + '/readme.md')

        # Now set up the sending factory.
        self.factory = ServerFactory()
        self.factory.service = self
        self.factory.protocol = Protocol

        port = reactor.listenTCP(0, self.factory, interface='')

        self.listen = port
        self.port = port.getHost().port
        self.host = port.getHost().host

    def GetInfo(self):

        return ('tarstream', self.port)

    def finished(self, _, transport):

        transport.loseConnection()

class FileSender(common):
    '''
    This uses the tartransfer library to send files.
    '''
    def Start(self, transport):
        '''
        This gets called by the :class:`.Protocol` with the transport.
        '''

        send = sender.Sender()
        print 'Sending:', self.folder
        d = send.beginTransfer(transport, self.folder)

        self.listen.stopListening()

        d.addCallback(self.finished, transport)

class FileReceiver(common):
    '''
    This uses the tartransfer library to get files.
    '''
    def Start(self, transport):

        self.receiver = client.Client(self.folder)

        self.receiver.registerProducer(transport, True)

        self.listen.stopListening()
