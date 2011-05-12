'''
Created on 23 Apr 2011

@author: Thomas Purchas

This module handles the FTP side of things. This is how we transfer files.
'''

from twisted.protocols.ftp import FTPFactory, FTPRealm
from twisted.cred.portal import Portal
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse

class FolderDB(InMemoryUsernamePasswordDatabaseDontUse): pass

class FTPServer(FTPFactory):
    
    def __init__(self, service):
        
        self.service = service
        
        self.FDB = FolderDB()
        p = Portal(FTPRealm("", "JobLocation"),
                   [self.FDB])
        
        FTPFactory.__init__(self, p)
        
    def addFolder(self, folder, password):
        
        self.FDB.addUser(folder, password)
        
    def removeFolder(self, folder):
        
        self.FDB.users.pop(folder)
