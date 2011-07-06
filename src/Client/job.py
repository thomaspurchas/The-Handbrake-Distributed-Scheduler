'''
Created on 14 May 2011

@author: Thomas Purchas
'''
from twisted.internet import defer
import tempfile
import os
import Handbrake

class job(object):
    '''
    Local job objects. These contain all of the code to coordinate handbrake
    management and files. 
    '''


    def __init__(self, service, HBJob):
        '''
        Takes a HBJob reference and wraps it up.
        '''
        self.service = service
        self.raw = HBJob
        self.dir = tempfile.mkdtemp()
        self.original = os.path.join(self.dir, 'original')
        self.final = os.path.join(self.dir, 'final')

        self.args = ''

        self.hbManager = None

        os.mkdir(self.original)
        os.mkdir(self.final)

        print 'New Job!!'

    def transferFilesToHere(self):

        self.raw.callRemote('setStage', 2)
        d = self.raw.callRemote('serveFiles')
        d.addCallback(self.service.fileFromServerTo, self.original)

        return d

    def getArgs(self):

        def setArgs(args):
            self.args = args

            return None

        d = self.raw.callRemote('getArgs')
        d.addCallback(setArgs)

        return d

    def startHandbrake(self, _):
        '''
        We now have the files and the handbrake arguments. Now time to start 
        Quattro and get encoding. 
        
        The returned deferred will get called when the transcoding completes.
        '''

        self.hbManager = Handbrake.Manager(self.args, self.raw)

        print 'We got args:', self.args
        print 'and files at:', self.original

        d = defer.succeed(None)
        return d
        #return self.hbManager.start()

    def start(self):
        '''
        Starts this job. The returned deferred will get called when the job 
        completes.
        '''

        def checkResults(Results):
            for success, _ in Results:
                if not success:
                    raise Exception('REPLACE, The file transfer was not successful')

            return None

        transfer = self.transferFilesToHere()
        args = self.getArgs()

        dList = defer.DeferredList([transfer, args])

        dList.addCallback(checkResults)
        dList.addCallback(self.startHandbrake)

        d = defer.Deferred()

        dList.chainDeferred(d)

        return d

    def stop(self):
        print 'Asked to stop job'
