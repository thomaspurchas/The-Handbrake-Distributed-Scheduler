'''
Created on 14 May 2011

@author: Thomas Purchas
'''
from twisted.spread import pb

class HBClient(pb.Refernceable):
    '''
    Client object
    '''

    def __init__(self, service):
        self.service = service
        
    def remote_queueUpdate(self):
        print 'queueUpdate called'
    
    def remote_stopJob(self, Job):
        print 'stopJob called with', Job
    
    def remote_shutdown(self):
        print 'shutdown called'
        
