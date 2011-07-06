'''
Created on 6 Jul 2011

@author: Thomas Purchas
'''
from twisted.internet.protocol import ServerFactory, Protocol
from tartransfer import sender

class Protocol(Protocol):
    
    def connectionMade(self):
        
        self.factory.service.Send(self.transport)
        
        

class FileSender(object):
    '''
    classdocs
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
    
    def Send(self, transport):
        '''
        This gets called by the :class:`.Protocol` with the transport.
        '''
        
        sender = sender.Sender()
        
        sender.beginTransfer(transport, self.folder)
        
        self.port.stopListening()
        
        
class FileReceiver(object):pass
        
