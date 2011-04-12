:mod:`HBClasses` --- Documentation on the basic classes
=======================================================

These classes makes up the basic set of class used for communication.

.. module:: HBClasses

.. class:: HBClient()

	This identifies the client.
	
	.. method:: remote_queueUpdate()
	
		This is called to tell the client that we have changed their
		queue.
		
	.. method:: remote_stopJob(Job)
		
		This is called to get a client to stop working on a job.
		
		:param Job: The job to stop working on.
		:type Job: :class:`.HBJob`
		
	.. method:: remote_shutdown()
	
		The server is shutting down. All clients should stop work and
		exit.
	
.. class:: HBQueue()

	This holds a load of :class:`.HBJob`\s and is passed to the
	clients so they know what to do.
	
	.. method:: remote_getJobs()
	
		This get a dictionary of jobs from the server. The
		dictionary keys give order, or something like that.
		
		:returns: Dictionary of jobs
		:rtype: :class:`dict`
	
.. class:: HBJob()

	This tells the client to do a specific task. These should have
	some sort of hierarchy to allow jobs to happen simultaneously.
	e.g. download one raw file while transcoding another.
	
	.. method:: remote_getFile()
	
		Get the file related to this job. This needs to be expanded
		to except more than one file.
		
		Read :ref:`spec-sendingfiles` for more info.
		
	.. method:: remote_returnFile()
	
		Return the finished product.
		
		Read :ref:`spec-sendingfiles` for more info.
		
	.. method:: remote_getProfile()
	
		Get the profile to give to handbrake.
		
		:returns: A dictionary with the nessary details that need
			to be passed onto HandBrake.
		:rtype: :class:`dict`