:mod:`HBClasses` --- Documentation on the basic classes
=======================================================

These classes makes up the basic set of class used for communication.

.. module:: HBClasses

.. class:: HBClient()

    This identifies the client.
    
    ..  method:: remote_queueUpdate()
    
        This is called to tell the client that we have changed their
        queue.
        
        Clients should now call :meth:`.remote_getJobs` to see what
        has changed.
        
        ..  note::
            It is possiable to compare referance objects and get a
            meaningful result. To using ``==`` to work out what jobs
            have been added or removed is viable.
            
            ..  note::
                This is achived by twisted using the ``.luid`` attribute.
        
    ..  method:: remote_stopJob(Job)
        
        This is called to get a client to stop working on a job.
        
        :param Job: The job to stop working on.
        :type Job: :class:`.HBJob`
        
    ..  method:: remote_shutdown()
    
        The server is shutting down. All clients should stop work and
        exit.
    
..  class:: HBQueue()

    This holds a load of :class:`.HBJob`\'s and is passed to the
    clients so they know what to do.
    
    ..  method:: remote_getJobs()
    
        This gets a list of assined :class:`.HBJob`\s from the server.
        The :class:`.HBJob` in index 0 should be executed first.
        
        :returns: List of :class:`HBJob`\'s.
        :rtype: :class:`list`
    
..  class:: HBJob()

    This tells the client to do a specific task. These should have
    some sort of hierarchy to allow jobs to happen simultaneously.
    e.g. download one raw file while transcoding another.
    
    ..  method:: remote_serveFiles()

        Instructs the server to make the files nessary for the job 
        avilable in an FTP location.
        
        The location returned will be a folder location, all files
        contained within are nessary for the job.
    
        Read :ref:`spec-sendingfiles` for more info.
        
        :returns: A URL to the FTP location of the format ftp://server:port/location
        :rtype: :data:`string`
        
    ..  method:: remote_returnFiles()
    
        Instructs the server to open up an FTP location to return 
        the file to.
        
        Read :ref:`spec-sendingfiles` for more info.
        
        :returns: A URL to the FTP location of the format ftp://server:port/location
        :rtype: :data:`string`
        
    ..  method:: remote_getArgs()
    
        Gets the list of arguments that need to be passed to handbrake. The list just
        needs to be prepended with a process name after which it can be pass stright
        to :meth:`.reactor.spawnProcess` as the `arg` keyword argument.
        
        :returns: :meth:`reactor.spawnProcess` `arg` list
        :rtype: :class:`list`
        
    ..  method:: remote_setStage(Stage)
    
        This method sets the state of the job. The stage is an
        interger number between 1 and 5 which have the following
        meaning:
        
        ======  =====================   ===============================================================
        Number  Short Description       Long Description
        ======  =====================   ===============================================================
          1     Queued                  Nothing has happened to it, this is a jobs initial state
          2     Transfering to client   The jobs files are currently being transfered to a client
          3     Transcoding             The job is currenlty being transcoded and is in progress
          4     Transfering to server   The jobs files are being transfered back after transcoding
          5     Complete                The job is complete. All resulting files are back at the server
        ======  =====================   ===============================================================
        
        :param Stage: The current stage of the job
        :type Stage: :data:`int`
            
    ..  method:: remote_setPercentage(Percentage)
        
        This sets the percentage complete of the jobs current stage.
        
        :param Percentage: Percent complete (0 - 100)
        :type Percentage: :data:`int`
        
    ..  method:: remote_setETA(Time)
    
        Set the time till completion of the current stage.
        
        :param Time: Time till completion in seconds.
        :type Time: :data:`int`
        
    ..  method:: remote_setSpeed(Speed)
    
        Set the speed of the current stage. The unit of speed changes
        depending on the stage.
        
        ======= ====
        Stage   Unit
        ======= ====
        2 and 4 MB/s
          3     FPS
        ======= ====
        
        :param Speed: Speed of current stage
        :type Speed: :data:`int`