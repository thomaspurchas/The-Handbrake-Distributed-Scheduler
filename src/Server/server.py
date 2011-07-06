'''
Created on 15 May 2011

@author: Thomas Purchas
'''
import sys
sys.path.append('C:\\Users\\Thomas Purchas\\Python\\HandbrakeDis-git\\src')

from service import serverService
from HBClasses import HBServer
from twisted.spread import pb
from twisted.internet import reactor
from twisted.python import log

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    service = serverService()
    factory = pb.PBServerFactory(HBServer(service))

    reactor.listenTCP(8789, factory)
    print 'Listening'
    reactor.run()

