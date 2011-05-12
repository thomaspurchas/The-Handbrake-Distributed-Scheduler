'''
Created on 23 Apr 2011

@author: Thomas Purchas
'''
from twisted.spread import pb

class HBServer(pb.Root):
    '''
    classdocs
    '''

    def __init__(self, service):
        
        self.service = service

    def remote_getQueue(self, Client):
        
        return self.service.createQueue(Client)
    
    def remote_sendClient(self, Client):
        '''
        Do something usefull
        @param Client:
        '''
        
        pass

class HBQueue(pb.Referenceable):
    
    def __init__(self, Client, Jobs=None):
        
        self.Client = Client
        
        if Jobs == None:
            self.jobs = []
        elif isinstance(Jobs, []):
            self.jobs = Jobs
            
        else:
            raise TypeError('Jobs must be a list')
    
    def addJob(self, Job):
        
        self.jobs.append(Job)
        self.client.callRemote("queueUpdate")
        
    def removeJob(self, Job):
        
        try:
            self.jobs.remove(Job)
        except:
            raise ValueError('That job is not in this list')
    
    def remote_getJobs(self):
        
        return self.jobs
        
class HBJob(pb.Referenceable):
    
    def __init__(self, service, Folder, args=["HandBrake"]):
        '''
        Create a new :class:`.HBJob`.
        
        :param Folder: The folder containing all the files for this job.
        :param args: The args that need to be passed to HandBrake
        '''
        
        self.args = args
        self.folder
        
        self.stage = 1
        self.percent = 0
        self.speed = 0
        self.eta = None
        
        self.service = service
    
    def remote_serveFiles(self):
        
        return self.service.serveFiles(self.folder + '/input', 'password')
        
    def remote_returnFiles(self): 
        
        return self.service.returnFiles(self.folder + '/output', 'password')
        
    def remote_getArgs(self):
        
        return self.args
    
    def remote_setStage(self, Stage):
        
        self.stage = Stage
    
    def remote_setPercentage(self, Percentage):
        
        self.percent = Percentage
    
    def remote_setETA(self, Time):
        
        self.eta = Time
        
    def remote_setSpeed(self, Speed):
        
        self.speed = Speed
