'''
Created on 15 May 2011

@author: Thomas Purchas
'''
import sys
sys.path.append('C:\\Users\\Thomas Purchas\\Python\\HandbrakeDis-git\\src')

from service import clientService
from twisted.spread import pb
from twisted.internet import reactor
from twisted.python import log

sys.path.append('C:\\Users\\Thomas Purchas\\Python\\HandbrakeDis-git\\src')

def bugger(fail):
    print fail

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    service = clientService('localhost')
    factory = pb.PBClientFactory()

    reactor.connectTCP(service.serverAddress, 8789, factory)

    d = factory.getRootObject()
    d.addCallback(service.serverConnected)
    d.addErrback(bugger)

    reactor.run()


