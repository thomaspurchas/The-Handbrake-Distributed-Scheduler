'''
Created on 18 May 2011

@author: Thomas Purchas
'''
from twisted.internet import defer, reactor
from twisted.internet.protocol import Protocol, ServerFactory
import threading 
import socket
import tarfile

class protocol(Protocol):
    
    def __init__(self):
        self.buffer = ''
        self.paused = False
        self.finished = False
    
    def dataReceived(self, data):
            
        self.service.sendData(data)
    
    def connectionMade(self):
        #print 'connectionMade'
        self.service.connectionMade(self)
        
    def connectionLost(self, failure):
        #print 'DONE2'
        self.service.finished()
        
    def stop(self):
        #print 'SERVER: Told to stop!'
        self.transport.loseConnection()
        self.buffer = ''

class tarThread(threading.Thread):
    
    def __init__(self, port, item, compression):
        
        threading.Thread.__init__(self)
        
        self.port = port
        self.item = item
        self.compression = compression
    
    def run(self):
        #print 'THREAD START'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        sock.connect(('localhost', self.port))
        # Shutdown the reading half of the socket
        #sock.shutdown(socket.SHUT_RD)
        #print 'SOCK CONNECTED CLIENT SIDE'
        fileobj = sock.makefile()
        
        tar = tarfile.open(fileobj=fileobj, mode='w|' + self.compression)
        
        tar.add(self.item)
        tar.close()
        fileobj.close()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        
        #print 'DONE'
        

class Sender(object):
    '''
    This provides a asynchronous interface for folder streaming that provides
    a twisted producer interface.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        self.fac = ServerFactory()
        self.fac.protocol = protocol
        self.fac.protocol.service = self
        
        port = reactor.listenTCP(0, self.fac, interface='localhost')
        
        self.listen = port
        self.port = port.getHost().port
        
        self.lastchunk = False
        
    def beginTransfer(self, consumer, item, compression=''):
        '''
        '''
        
        if compression not in ('bz2', 'gz', ''):
            raise ValueError('%s is an invalid compression algorithm' % compression)
        
        self.item = item
        
        self.consumer = consumer
        
        self.deferred = d = defer.Deferred()
        
        self.thread = tarThread(self.port, self.item, compression)
        self.thread.start()
        
        return d
        
    def connectionMade(self, proto):
        
        self.listen.stopListening()
        
        self.protocol = proto
        
        self.consumer.registerProducer(self, True)
     
    def finished(self):
         
        self.consumer.unregisterProducer()
        self.deferred.callback(None)
     
    def sendData(self, data):
        
        self.consumer.write(data)
        
    def resumeProducing(self):
        #print 'SERVER: Resume'
        self.protocol.transport.resumeProducing()
    
    def pauseProducing(self): 
        #print 'SERVER: Pause'
        self.protocol.transport.pauseProducing()
    
    def stopProducing(self): 
        #print 'SERVER: stopProducing'
        self.protocol.stop()
        self.deferred.errback(None)
        
class testC(object):
    
    def registerProducer(self, pro, stream):
        
        self.pro = pro
        self.file = open('test.tar', mode='wb')
        self.printstuff()
        
    def unregisterProducer(self):
        
        reactor.stop()
        
    def write(self, data):
        
        self.data = data
        
    def __str__(self):
        self.pro.resumeProducing()
        return self.data
    
    def printstuff(self):
        self.pro.resumeProducing()
        
        self.file.write(self.data)
        
        self.call = reactor.callLater(0, self.printstuff)
        
if __name__ == '__main__':
    
    s = Sender()
    c = testC()
    
    s.beginTransfer(c, '.', 'bz2')
    
    #reactor.callWhenRunning(c.printstuff())
    reactor.run()
