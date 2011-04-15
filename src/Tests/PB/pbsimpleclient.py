
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.spread import pb
from twisted.internet import reactor
from twisted.python import util
import inspect

def thing(a):
    c = a[2]
    b = a[1]
    a = a[0]
    c.luid = a.luid
    print a == b
    print b == c 
    print inspect.getmembers(a)
    print inspect.getmembers(b)
    print inspect.getmembers(c)

factory = pb.PBClientFactory()
reactor.connectTCP("localhost", 8789, factory)
d = factory.getRootObject()
d.addCallback(lambda object: object.callRemote("echo", {'Hello':23, 'Network':'234'}))
d.addCallback(thing)
d.addErrback(lambda reason: 'error: ' + str(reason.value))
d.addCallback(util.println)
d.addCallback(lambda _: reactor.stop())
reactor.run()
