agutil
======

-  Master build status: |Master Build Status| |Live Package Version|
-  Development build status: |Dev Build Status| |Dev Coverage Status|

A collection of python utilities

**Version:** 4.0.2

Tools:
      

-  search\_range (A utility for manipulating numerical ranges)
-  status\_bar (A simple progress bar indicator)
-  Logger (A class for fast, simple, logging)
-  ActiveTimeout (A class for enforcing a timeout for a set of
   operations)
-  Several standalone utility methods (See the `agutil module
   page <https://github.com/agraubert/agutil/wiki/agutil-%28main-module%29>`__
   on the wiki)

The **io** package:

-  Socket (A low-level network IO class built on top of the standard
   socket class)
-  SocketServer (A low-level listen server to accept connections and
   return Socket classes)
-  MPlexSocket (A low-level network IO class which multiplexes I/O
   through multiple channels. Threadless version of ``QueuedSocket``)
-  [STRIKEOUT:QueuedSocket (A low-level network IO class built to manage
   input across multiple channels)]

**Deprecated: Will be removed in a future release.** Please transition
to ``agutil.io.MPlexSocket`` which is a threadless version of the same
interface

The **parallel** package:

-  parallelize (A decorator to easily convert a regular function into a
   parallelized version)
-  parallelize2 (A similar parallelization decorator with a slightly
   different flavor)
-  IterDispatcher (Logical backend for dispatching calls with
   parallelize)
-  DemandDispatcher (Logical backend for dispatching calls with
   parallelize2)
-  ThreadWorker (Task management backend for dispatching parallel calls
   to threads)
-  ProcessWorker (Task management backend for dispatching parallel calls
   to processes)

The **security** package:

-  SecureSocket (A mid-level network IO class built to manage encrypted
   network communications)
-  SecureConnection (A high-level, multithreaded class for sending and
   receiving encrypted files and messages)
-  SecureServer (A low-level listen server to accept connections and
   return SecureConnection instances)
-  agutil-secure (A command line utility for encrypting and decrypting
   files)
-  EncryptionCipher and DecryptionCipher (Twin classes for agutil's
   modular encryption format)
-  Several other utility functions and classes for encrypting and
   decrypting data

Documentation:
--------------

Detailed documentation of these packages can be found on the `agutil
Github wiki page <https://github.com/agraubert/agutil/wiki>`__

.. |Master Build Status| image:: https://travis-ci.org/agraubert/agutil.svg?branch=master
   :target: https://travis-ci.org/agraubert/agutil
.. |Live Package Version| image:: https://img.shields.io/pypi/v/agutil.svg
   :target: https://pypi.python.org/pypi/agutil
.. |Dev Build Status| image:: https://travis-ci.org/agraubert/agutil.svg?branch=dev
   :target: https://travis-ci.org/agraubert/agutil
.. |Dev Coverage Status| image:: https://coveralls.io/repos/github/agraubert/agutil/badge.svg?branch=dev
   :target: https://coveralls.io/github/agraubert/agutil?branch=dev
