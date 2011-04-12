
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.spread import pb
from twisted.internet import reactor
from twisted.python import util

factory = pb.PBClientFactory()
reactor.connectTCP("localhost", 8789, factory)
d = factory.getRootObject()
d.addCallback(lambda object: object.callRemote("echo", {'Hello':23, 'Network':'234'}))
d.addCallback(lambda echo: 'server echoed: ' + repr(echo))
d.addErrback(lambda reason: 'error: ' + str(reason.value))
d.addCallback(util.println)
d.addCallback(lambda _: reactor.stop())
reactor.run()
