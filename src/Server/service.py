'''
Created on 23 Apr 2011

@author: Thomas Purchas
'''
from HBClasses import HBJob, HBQueue
import TarSendFiles

class serverService(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.jobs = []
        self.queues = []
        self.clients = []

    def newClient(self, Client):
        self.clients.append(Client)

    def connectionFail(self, Failure, Client=None):
        '''
        Something has gone wrong some where. We shall print the traceback and
        kill the client.
        '''
        Failure.printTrackback()
        if Client != None:
            Client.callRemote('shutdown')

    def serveFiles(self, Folder):
        sender = TarSendFiles.FileSender(Folder)
        return sender.GetInfo()

    def returnFiles(self, Folder):
        receiver = TarSendFiles.FileReceiver(Folder)
        return receiver.GetInfo()

    def createJob(self, SomeInfo):
        job = HBJob(self, *SomeInfo)

        self.jobs.append(job)

        self.queueJobs()

    def updateClients(self):
        '''
        Tell all the clients to update there queues.
        '''

        for client in self.clients:

            client.callRemote('queueUpdate').addErrback(self.connectionFail, client)

    def createQueue(self, Client):

        Q = HBQueue(Client)

        self.queues.append(Q)

        return Q

    def queueJobs(self):

        for job in self.jobs:

            if job.queue != None:
                continue

            shortest = None

            for Q in self.queues:
                if shortest == None:
                    shortest = Q
                elif len(Q.jobs) < len(shortest.jobs):

                    shortest = Q

            shortest.addJob(job)

        self.updateClients()
