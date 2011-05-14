'''
Created on 14 May 2011

@author: Thomas Purchas
'''

class job(object):
    '''
    Local job objects. These contain all of the code to coordinate handbrake
    management and files. 
    '''


    def __init__(self, HBJob):
        '''
        Takes a HBJob reference and wraps it up.
        '''
        
        self.raw = HBJob
        
        print 'New Job!!'
    
    def stop(self):
        print 'Asked to stop job'
