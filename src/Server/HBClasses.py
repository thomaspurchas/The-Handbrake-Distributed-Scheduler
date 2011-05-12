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

    def remote_getQueue(self):
        
        return self.service.createQueue()
    
    def remote_sendClient(self, Client):
        '''
        Do something usefull
        @param Client:
        '''
        
        pass

class HBQueue(pb.Referenceable):
    
    def __init__(self, Jobs=None):
        
        if Jobs == None:
            self.jobs = []
        elif isinstance(Jobs, []):
            self.jobs = Jobs
            
        else:
            raise TypeError('Jobs must be a list')
    
    def addJob(self, Job):
        
        self.jobs.append(Job)
        
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
        
        self.service.serveFolder(self.folder + '/input', 'password')
        
        return "ftp://" + self.service.netLocation + '/' + self.folder + '/input'
        
    def remote_returnFiles(self): 
        
        self.service.serveFolder(self.folder + '/output', 'password')
        
        return "ftp://" + self.service.netLocation + '/' + self.folder + '/output'
        
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
