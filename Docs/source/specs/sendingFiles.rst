.. _spec-sendingfiles:

Sending files
=============

We currently send files using my super awesome tar streaming library.
It uses the standard tar file library and wraps it up as a twisted 
consumer/producer depending on what end your at. 

It then feeds files into the tar library to create a tar stream 
which is then pushed down the pipe. At the other end the stream is
pushed into the tar library there to be turned back into files.

By using this library it would be possiable to turn on bzip, or 
gzip compression. However I suspect that the savings would be minimal.
