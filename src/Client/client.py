'''
Created on 15 May 2011

@author: Thomas Purchas
'''
from service import clientService
from twisted.spread import pb
from twisted.internet import reactor
from twisted.python import log 
import sys

def bugger(fail):
    print fail

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    service = clientService()
    factory = pb.PBClientFactory()
    
    reactor.connectTCP('localhost', 8789, factory)
    
    d = factory.getRootObject()
    d.addCallback(service.serverConnected)
    d.addErrback(bugger)
    
    reactor.run()


