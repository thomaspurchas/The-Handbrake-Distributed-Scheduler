Protocol --- A description of how we communicate
================================================

Because we have both ends of the wire  we are going to use twisted's
`Perspective Broker`__ (PB) protocol.

This should allow us to perform remote procedure calls.

However PB_ is not designed for large files, not will it take them
(limits will stop us), so to transfer files between clients we will 
use an FTP server and client pair. Both of these will be hosted by
twisted.

PB_ objects
===========

There are two major classes of objects that are involved, 
`Server side`_ and `Client side`_. Obviously server side objects
are found on the server and client side on the client.

Server side
~~~~~~~~~~~

The server side objects are responsible for handling client
identities and there current status. 

On connection a :class:`HBQueue` object is created on the server and
passed back to the client. This objects references the jobs assigned to
the client, and the client is then responsible for carrying out the
jobs.

Along side the :class:`HBQueue` object there exist :class:`.HBJob`
objects. These objects contain information on what needs to be done,
and provide remote calls to allow the client to request resources 
from the server required to complete a job.

Client side
~~~~~~~~~~~

The client side objects exists just allow the server to control them.
Using client side objects the server can force the client to send a
status update, or get it to stop a job etc.

After the client connects and retrieves its :class:`HBQueue` object
reference, it creates a :class:`.HBClient` object which is passed back
to the server. This object allows the server to instruct the client
to stop partial jobs, or force a status update etc.

Note:
=====

We have this the wrong way around. When the client connects it can
request the root object from the server. After that the client
can pass an object to the server using remote calls on the root
objects.

This would mean that when we connect the client would get the remote
object, then register with the server by passing it a
:class:`.HBClient` object, and get :class:`HBQueue` object in
return.

From here the server would add new :class:`HBJob` items to
:class:`.HBQueue` objects. From here it use the :class:`HBClient`
objects to inform the clients of an update to their
:class:`.HBQueue`.

The client then retrieves the new info, and starts working on the new
:class:`HBJob`, or leaves it in waiting. Where the server may then
decided to reshuffle the :class:`HBJob` objects between 
:class:`HBQueue`\s.

.. _PB: http://twistedmatrix.com/documents/current/core/howto/pb-intro.html
__ PB_