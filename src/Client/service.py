'''
Created on 14 May 2011

@author: Thomas Purchas
'''
from twisted.internet import reactor
from job import job
import HBClasses
import transfer

class clientService(object):
    '''
    The client service that will manage everything.
    '''


    def __init__(self, serverAddress):
        '''
        Constructor
        '''
        self.serverAddress = serverAddress

        self.jobs = []
        self.rawJobs = []
        self.queue = None
        self.HBClient = HBClasses.HBClient(self)
        self.currentjob = None

    def connectionFail(self, Failure):
        '''
        This is a bog standard error handler that just prints the failure kills
        the reactor. This need further improvement in the future, but it will do
        for now.
        '''

        Failure.printTraceback()
        reactor.stop()

        return None

    def serverConnected(self, serverObject):
        '''
        We have connected to the server, this means that we can use the
        serverObject and grab useful things like jobs etc.
        '''
        print 'Connected'
        def queueStore(queue):
            '''
            Store the queue, but also call getJobs
            '''
            d = queue.callRemote('getJobs')
            d.addCallbacks(self.sortJobs, self.connectionFail)
            self.queue = queue

        self.server = serverObject

        serverObject.callRemote('sendClient', self.HBClient).addErrback(self.connectionFail)

        d = serverObject.callRemote('getQueue', self.HBClient)

        d.addCallbacks(queueStore, self.connectionFail)

    def shutdown(self):
        '''
        That's it. Game over. The shit has hit the fan, and it time to say bye 
        bye.
        
        To shutdown we stop the reactor. This will close all our sockets, and
        stop the flow of callbacks. But it will give things a bit of time to
        stop.
        '''

        reactor.stop()

    def stopJob(self, Job):
        '''
        Have a look at all of our jobs. If it's running tell it to stop, else
        just kill the ref.
        '''

        for j in self.jobs:
            if Job == j.raw:
                j.stop()
                break

        else:
            if self.currentjob.raw == Job:
                self.currentjob.stop()
                self.startAJob()
            else:
                raise Exception('We got told to stop a job we don''t have!!')

    def startAJob(self, *args, **kargs):
        '''
        Get the jobs rolling.
        '''
        def finished(_):
            self.currentjob = None

        if len(self.jobs) == 0:
            print 'No more jobs!'

        else:
            self.currentjob = self.jobs.pop()

            d = self.currentjob.start()
            d.addCallback(finished)
            d.addCallback(self.startAJob)

    def sortJobs(self, Jobs):
        '''
        This takes a list of job references from the server, and filters them
        to get the new ones. From there is passes them them to the local job
        objects to be managed.
        '''
        newjobs = []
        for j in Jobs:
            if not (j in self.rawJobs):
                self.rawJobs.append(j)
                newjobs.append(j)

        for j in newjobs:
            self.jobs.append(job(self, j))

        if self.currentjob == None:
            self.startAJob()

    def updateQueue(self):
        '''
        Update our job queue.
        '''
        if self.queue != None:
            d = self.queue.callRemote('getJobs')
            d.addCallbacks(self.sortJobs, self.connectionFail)

    def fileFromServerTo(self, details, location):
        print 'Got transfer request:', details
        if not hasattr(transfer, 'xfer_' + details[0]):
            raise Exception('REPLACE, We do not support that transfer method')

        else:
            agent = getattr(transfer, 'xfer_' + details[0])

            return agent(location, self, self.serverAddress, *details[1:])

