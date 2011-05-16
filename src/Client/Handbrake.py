'''
Created on 16 May 2011

@author: Thomas Purchas
'''

class Manager(object):
    '''
    This is a management class for looking after Handbrake. Inisalising this
    sets in motion the process of setting up a handbrake process and setting it
    going. 
    '''


    def __init__(self, args, remoteJob):
        '''
        Takes an args argument. This should contain all the necessary arguments
        to set Handbrake running, and in the same format that a twisted process
        reactor expects.
        
        Also expect the remoteJob object so that is can report its progress
        directly to the server.
        '''
        
