'''
Created on 23 Apr 2011

@author: Thomas Purchas
'''
from HBClasses import HBJob, HBQueue

class HBservice(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.jobs = []
        self.queues = []
        
    def netLocation(self): pass
    
    def serveFolder(self, Folder): pass
    
    def createJob(self, SomeInfo):
        
        job = HBJob(*SomeInfo)
        
        self.jobs.append(job)
        
        self.queueJobs()
        
    def createQueue(self):
        
        Q = HBQueue()
        
        self.queues.append(Q)
        
        return Q 
        
    def queueJobs(self):
        
        for job in self.jobs:
            
            shortest = None
            
            for Q in self.queues:
                if shortest == None:
                    shortest = Q
                elif len(Q.jobs) < len(shortest.jobs):
                    
                    shortest = Q
        
            shortest.addJob(job)
