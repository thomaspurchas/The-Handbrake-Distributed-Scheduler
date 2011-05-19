'''
Created on 19 May 2011

@author: Thomas Purchas
'''

from sender import Sender
from client import Client
from twisted.internet import reactor

def stop(_): reactor.stop()

if __name__ == '__main__':
    C = Client('../Tests/tartransfer')
    S = Sender()
    
    S.beginTransfer(C, '../', '').addCallback(stop)
    
    reactor.run()
