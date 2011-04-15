
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.spread import pb
from twisted.internet import reactor

class Two(pb.Referenceable):
    def remote_thing(self):
        print 'Thing called'

class Echoer(pb.Root):
    def remote_echo(self, st):
        print 'echoing:', st
        a = Two()
        b = Two()
        return [a, a, b]

if __name__ == '__main__':
    reactor.listenTCP(8789, pb.PBServerFactory(Echoer()))
    reactor.run()
