.. django-dbbackup documentation master file, created by
   sphinx-quickstart on Sun May 18 13:35:53 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-dbbackup's documentation!
===========================================

Contents:

.. toctree::
   :maxdepth: 1

   installation
   configuration
   dropbox
   s3
   ftp
   local storage
   
Management Commands
-------------------

dbbackup
~~~~~~~~
Backup your database to the specified storage. By default this
will backup all databases specified in your settings.py file and will not
delete any old backups. You can optionally specify a server name to be included
in the backup filename.

::

    dbbackup [-s <servername>] [-d <database>] [--clean] [--compress] [--encrypt]

dbrestore
~~~~~~~~~

Restore your database from the specified storage. By default
this will lookup the latest backup and restore from that. You may optionally
specify a servername if you you want to backup a database image that was
created from a different server. You may also specify an explicit local file to
backup from.

::

    dbrestore [-d <database>] [-s <servername>] [-f <localfile>]

mediabackup
~~~~~~~~~~~~
Backup media files. Default this will backup the files in
the MEDIA_ROOT. Optionally you can set the DBBACKUP_MEDIA_PATH setting.

::

    mediabackup [--encrypt] [--clean] [--servername <servername>]


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

