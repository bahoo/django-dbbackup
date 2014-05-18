Django Database Backup
======================

This Django application provides management commands to help backup and
restore your project database to AmazonS3, Dropbox or Local Disk.

-  Keep your important data secure and offsite.
-  Use Crontab or Celery to setup automated backups.
-  Great to keep your development database up to date.

DATABASE SETTINGS
=================

The following databases are supported by this application. You can
customize the commands used for backup and the resulting filenames with
the following settings.

NOTE: The {adminuser} settings below will first check for the variable
ADMINUSER specified on the database, then fall back to USER. This allows
you supplying a different user to perform the admin commands dropdb,
createdb as a different user from the one django uses to connect. If you
need more fine grain control you might consider fully customizing the
admin commands.