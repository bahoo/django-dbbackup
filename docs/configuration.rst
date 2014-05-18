Configuration
=============

General settings
----------------

DBBACKUP_DATABASES
~~~~~~~~~~~~~~~~~~

List of key entries for ``settings.DATABASES`` which shall be used to
connect and create database backups.

Default: ``list(settings.DATABASES.keys())`` (keys of all entries listed)

DBBACKUP_BACKUP_DIRECTORY
~~~~~~~~~~~~~~~~~~~~~~~~~

Where to store backups

Default: ``os.getcwd()`` (Current working directory)

DBBACKUP_CLEANUP_KEEP and DBBACKUP_CLEANUP_KEEP_MEDIA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When issueing ``dbbackup`` and ``mediabackup``, old backup files are
looked for and removed.

Default: ``10`` (days)

DBBACKUP_MEDIA_PATH
~~~~~~~~~~~~~~~~~~~

Default: settings.MEDIA_ROOT

DBBACKUP_DATE_FORMAT
~~~~~~~~~~~~~~~~~~~~

Date format to use for naming files (only currently used in mediabackup).

Default: ``'%Y-%m-%d-%H%M%S'``

DBBACKUP_SERVER_NAME
~~~~~~~~~~~~~~~~~~~~

Some weird server name that can be given and will be used in backed
up files -- this is nice when you have many projects backed up in the
same directory.

Default: ``''``


DBBACKUP_FILENAME_TEMPLATE

Postgresql
----------

DBBACKUP_POSTGRESQL_RESTORE_SINGLE_TRANSACTION
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When doing a restore with postgres, wrap everything in a single transaction
so that errors cause a rollback.

Default: ``True``

DBBACKUP_POSTGIS_SPACIAL_REF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When on Postgis, using this setting currently disables
``CREATE EXTENSION POSTGIS;``. Ideally, it should run the good old Postgis
templates for version 1.5 of Postgis.
