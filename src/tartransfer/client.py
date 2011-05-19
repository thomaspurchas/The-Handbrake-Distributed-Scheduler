'''
Created on 19 May 2011

@author: Thomas Purchas
'''

import threading
import socket
import tarfile
import os
from twisted.internet.protocol import Protocol, ServerFactory
from twisted.internet import reactor, defer

class protocol(Protocol):
    
    def __init__(self): pass
    
    def connectionMade(self):
        #print 'CLIENT: connectionMade'
        self.service.connectionMade(self.transport)
        
    def connectionLost(self, falure): pass
        #print 'CLIENT: connectionLost'
        
class tarThread(threading.Thread):
    
    def __init__(self, port, where):
        
        threading.Thread.__init__(self)
        
        self.port = port
        self.where = where
    
    def safe(self, path):
               
        joined = os.path.join(self.where, path)
        abspath = os.path.abspath(joined)
        
        destpath = os.path.abspath(self.where)
        
        common = os.path.commonprefix([abspath, destpath])
        
        if common.startswith(destpath):
            return True
        
        return False
    
    def run(self):
        #print 'CLIENT: THREAD START'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        sock.connect(('localhost', self.port))
        # Close the sending half of the socket
        #sock.shutdown(socket.SHUT_WR)
        #print 'CLIENT: SOCK CONNECTED CLIENT SIDE'
        fileobj = sock.makefile()
        
        tar = tarfile.open(fileobj=fileobj, mode='r|*')
            
        while True:
            info = tar.next()
            
            if info == None:
                break
            
            if not self.safe(info.name): continue
                          
            tar.extract(info, self.where)
            
        tar.close()
        fileobj.close()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        
        #print 'CLIENT: DONE'

class Client(object):
    
    def __init__(self, path=''):
        
        self.fac = ServerFactory()
        self.fac.protocol = protocol
        self.fac.protocol.service = self
        
        self.path = path
        
        port = reactor.listenTCP(0, self.fac, interface='localhost')
        
        self.listen = port
        self.port = port.getHost().port
        
        self.thread = tarThread(self.port, self.path)
        
        self.deferred = defer.Deferred()
        
        self.transport = None
        
    def connectionMade(self, transport):
        
        self.listen.stopListening()
        self.transport = transport
        
        self.deferred.callback(transport)
        
    def addProducer(self, _, producer, streaming):
        
        self.transport.registerProducer(producer, streaming)
        
        if streaming:
            producer.resumeProducing()
    
    def registerProducer(self, Producer, Streaming):
        
        self.deferred.addCallback(self.addProducer, Producer, Streaming)
        self.thread.start()
        
        if Streaming:
            Producer.pauseProducing()
    
    def unregisterProducer(self):
    
        self.transport.unregisterProducer()
        self.finished()
    
    def finished(self):
        
        try:
            self.transport.loseConnection()
        except:
            pass
            
    def write(self, data):
        #print 'CLIENT: write'
        self.transport.write(data)
