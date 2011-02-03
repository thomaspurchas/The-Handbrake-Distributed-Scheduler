'''
Created on 7 Dec 2010

@author: Thomas Purchas
'''

from twisted.internet import protocol
from twisted.internet import reactor

import re



HANDBRAKECLIPATH = 'Handbrake\HandBrakeCLI.exe'
INPUTPATH = "Handbrake\\test.avi"
OUTPUTPATH = "Handbrake\\OutputTest.mp4"

class HandBrakeProcess(protocol.ProcessProtocol):
    def __init__(self, ProgressCallback, OutCallback, ErrorCallback, EndCallback):
        '''
        ProgressCallback will be passed 4 arguments:
            - Percentage Complete - Float or None
            - FPS - Float or None
            - Average FPS - Float or None
            - ETA - Time delta object or None
        
        
        ErrorCallback and OutCallback will be passed a string containing the 
        line sent by Handbrake.
        
        End Callback will be called when the handbrake process is called. It
        will be passed an integer containing the error code from handbrake
        '''
        # Store callback refs
        
        self.ProgressBack = ProgressCallback
        self.OutBack = OutCallback
        self.ErrBack = ErrorCallback
        self.EndBack = EndCallback
        
        # Check that the call backs are callable
        assert callable(self.ProgressBack)
        assert callable(self.OutBack)
        assert callable(self.ErrBack)
        assert callable(self.EndBack)
        
        
        # Set up self.line and self.rawdata for use later when stuff comes in.
        self.rawdata = ""
        
        self.rawerrdata = ""
        
        # Setup counts
        self.dataRecvCount = 0
        self.errRecvCount = 0
        
    def __SplitLines(self, data):
        '''
        Splits the string given to it into lines. It returns all of the lines 
        minus the last line if it did not end with a newline character.
        '''        
        lines = data.splitlines()
        
        return lines
        
    def ConnectionMade(self):
        
        print ' Connected to HandBrake. Closing STDIN'
        
        self.transport.closeStdin()
        
    def outReceived(self, data):
        # Got data from Stdin. 
        # print 'Got Data'
                
        # Now we look at the raw data and split it up into lines based on 
        # new line characters and also take out other such characters
          
        lines = self.__SplitLines(data)
                
        for line in lines:
            # Do analysis to see if we can extract data for the 
            # PercentageCallback
            if line.startswith('Encoding: '):
                # This is a good sign. Now for a super regex
                
                percentagepattern = '.*?(?P<Percent>[0-9]{1,3}\.[0-9]{2}) %'
                fpspattern = '(.*?\((?P<FPS>[0-9]+\.[0-9]{2}) fps'
                avgfpspattern = '.*?avg (?P<avgFPS>[0-9]+\.[0-9]{2}) fps'
                etapattern = '.*?ETA (?P<ETA>[0-9]+h[0-9]{2}m[0-9]{2}s))?'
                
                pattern = (percentagepattern + fpspattern 
                                                + avgfpspattern + etapattern)
                
                Match = re.match(pattern, line)
                
                if Match:
                    Percentage = Match.group('Percent')
                
                    FPS = Match.group('FPS')
                    avgFPS = Match.group('avgFPS')
                    ETA = Match.group('ETA')
                    
                    # Clean up the results and make them numbers
                    try:
                        Percentage = float(Percentage)
                        FPS = float(FPS)
                        avgFPS = float(avgFPS)
                    except TypeError:
                        # This means that something had a value of None which is
                        # fine.
                        pass
                    except ValueError:
                        # This means that we got a funny value we did not expect
                        # Set all values to None
                        Percentage, FPS, avgFPS, ETA = None, None, None, None
                    self.ProgressBack(Percentage, FPS, avgFPS, ETA)         
            
            self.OutBack(line)
        
        # Add one to dataRecv count
        self.dataRecvCount += 1
        
    def errReceived(self, data):
        
        # Now we look at the raw data and split it up into lines based on 
        # new line characters and also take out other such characters
          
        lines = self.__SplitLines(data)
                
        for line in lines:
            self.ErrBack(line)
                        
        # Add one to the errRecv count
        self.errRecvCount += 1
    
    def processExited(self, reason):
        # Handbrake ended. Call the EndCallback with the exit code
        try:
            self.EndBack(reason.value.exitCode)
        except:
            pass
       
              
        reactor.stop() #@UndefinedVariable

pp = HandBrakeProcess(None, None, None, None)

reactor.spawnProcess(pp, HANDBRAKECLIPATH, ["HandBrake", "-i", INPUTPATH, #@UndefinedVariable
                                             "-o", OUTPUTPATH])

reactor.run() #@UndefinedVariable
