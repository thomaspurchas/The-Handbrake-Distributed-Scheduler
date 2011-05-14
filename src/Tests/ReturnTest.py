'''
Created on 9 Jan 2011

@author: Thomas Purchas
'''
class test(object):
    
    def __hash__(self):
        return 1
    
    def __eq__(self, other):
        
        return 9
    
a = [test(), test(), test()]

if test() in a : print 'YES'
