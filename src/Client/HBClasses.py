'''
Created on 14 May 2011

@author: Thomas Purchas
'''
from twisted.spread import pb

class HBClient(pb.Referenceable):
    '''
    Client object
    '''

    def __init__(self, service):
        self.service = service
        
    def remote_queueUpdate(self):
        self.service.updateQueue()
        print 'queueUpdate called'
    
    def remote_stopJob(self, Job):
        self.service.stopJob(Job)
        print 'stopJob called with', Job
    
    def remote_shutdown(self):
        self.service.shutdown()
        print 'shutdown called'
        
