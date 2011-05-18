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
    
    def dataReceived(self, data):
        
        self.buffer += data
        
        if (len(self.buffer) >= 32000) and not self.paused:
            
            self.transport.pauseProducing()
            self.paused = True
            
    def getData(self):
        
        data = self.buffer
        self.buffer = ''
        
        if self.paused:
            self.transport.resumeProducing() 
            self.paused = False  
        
        return data
    
    def connectionMade(self):
        print 'connectionMade'
        self.service.connectionMade(self)
        
    def connectionLost(self, failure):
        print 'DONE2'
        self.service.finished()
        
    def stop(self):
        
        self.transport.loseConnection()
        self.buffer = ''

class tarThread(threading.Thread):
    
    def __init__(self, port, item):
        
        threading.Thread.__init__(self)
        
        self.port = port
        self.item = item
    
    def run(self):
        print 'THREAD START'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        sock.connect(('localhost', self.port))
        print 'SOCK CONNECTED CLIENT SIDE'
        fileobj = sock.makefile()
        
        tar = tarfile.open(fileobj=fileobj, mode='w|bz2')
        
        tar.add(self.item)
        tar.close()
        fileobj.close()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        
        print 'DONE'
        

class sender(object):
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
        
        self.lastchunk = None
        
    def beginTransfer(self, item, consumer):
        '''
        '''
        
        self.item = item
        
        self.consumer = consumer
        
        self.deferred = d = defer.Deferred()
        
        self.thread = tarThread(self.port, self.item)
        self.thread.start()
        
        return d
        
    def connectionMade(self, proto):
        
        self.listen.stopListening()
        
        self.protocol = proto
        
        self.consumer.registerProducer(self, False)
        
    def finished(self):
        
        self.lastchunk = self.protocol.getData()
        
    def resumeProducing(self):
        
        if self.lastchunk == None:
            data = self.protocol.getData()
            
        else:
            data = self.lastchunk
        
        self.consumer.write(data)
        
        if self.lastchunk != None:
            self.consumer.unregisterProducer()
    
    def pauseProducing(self): pass
    
    def stopProducing(self): 
        
        self.protocol.stop()
        
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
    
    s = sender()
    c = testC()
    
    s.beginTransfer('.', c)
    
    #reactor.callWhenRunning(c.printstuff())
    reactor.run()
