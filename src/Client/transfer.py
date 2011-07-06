'''
Created on 16 May 2011

@author: Thomas Purchas
'''
import TarGetFiles
def xfer_sockets(destination, service, host, port):
    '''
    This is the basic transfer method that uses sockets to transfer the raw
    data across the network using sockets. It cheats a little be by using tar
    files to wrap and compress the data.
    '''
    pass

def xfer_tarstream(destination, service, host, port):
    '''
    This transfer method uses the tartransfer library to send files over the
    wire using a tar stream.
    '''
    print 'Got tarstream transfer request. Port:', port, 'Host:', host
    print "Remember this don't work at the moment"

    trans = TarGetFiles.FileReceiver(destination, port, host)
    return trans.deferred
