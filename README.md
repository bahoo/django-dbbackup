# Django Database Backup #

This Django application provides management commands to help backup and
restore your project database to AmazonS3, Dropbox or Local Disk.

* Keep your important data secure and offsite.
* Use Crontab or Celery to setup automated backups.
* Great to keep your development database up to date.


# DATABASE SETTINGS #

The following databases are supported by this application. You can customize
the commands used for backup and the resulting filenames with the following
settings.

NOTE: The {adminuser} settings below will first check for the variable ADMINUSER
specified on the database, then fall back to USER. This allows you supplying a
different user to perform the admin commands dropdb, createdb as a different
user from the one django uses to connect.  If you need more fine grain control
you might consider fully customizing the admin commands.

## MySQL ##

**DBBACKUP_MYSQL_BACKUP_COMMANDS (optional)** -
   List of commands to use execute when creating a backup. Commands are sent
   to popen and should be split into shlex tokens. By default, the following
   command is run:

    mysqldump --user={adminuser} --password={password} --host={host} --port={port} {databasename} >

**DBBACKUP_MYSQL_RESTORE_COMMANDS (optional)** -
   List of commands to use execute when creating a backup. Commands are sent
   to popen and should be split into shlex tokens. By default, the following
   command is run:

    mysql --user={adminuser} --password={password} --host={host} --port={port} {databasename} <


## PostgreSQL ##

**DBBACKUP_POSTGRES_BACKUP_COMMANDS (optional)** -
   List of commands to use execute when creating a backup. Commands are sent
   to popen and should be split into shlex tokens. By default, the following
   command is run:

    pg_dump --username={adminuser} --host={host} --port={port} {databasename} >

**DBBACKUP_POSTGRES_RESTORE_COMMANDS (optional)** -
   List of commands to use execute when restoring a backup. Commands are sent
   to popen and should be split into shlex tokens. By default, the following
   commands are run:

    dropdb --username={adminuser} --host={host} --port={port} {databasename}
    createdb --username={adminuser} --host={host} --port={port} --owner={username} {databasename}
    psql --username={adminuser} --host={host} --port={port} --single-transaction {databasename} <


## SQLite ##

**DBBACKUP_SQLITE_BACKUP_COMMANDS (optional)** -
   List of commands to use execute when creating a backup. Commands are sent to
   popen and should be split into shlex tokens. By default, the following
   command is run:
   
    ['<READ_FILE>', '{databasename}']

**DBBACKUP_SQLITE_RESTORE_COMMANDS (optional)** -
   List of commands to use execute when restoring a backup. Commands are sent
   to popen and should be split into shlex tokens. By default, the following
   command is run:
   
    ['<WRITE_FILE>', '{databasename}']

------

# DEFINING BACKUP COMMANDS #

When creating backup or restore commands, there are a few template variables
you can use in the commands (listed below). Also note, ending a command with >
or < will pipe the file contents from or to the command respectively.

    {databasename}: Name of the database from settings.py
    {servername}: Optional SERVER_NAME setting in settings.py
    {datetime}: Current datetime string (see DBBACKUP_DATE_FORMAT).
    {extension}: File extension for the current database.

------

# GLOBAL SETTINGS #

**DBBACKUP_STORAGE (required)** -
   String pointing to django-dbbackup location module to use when performing a
   backup. You can see the exact definitions to use in the required settings
   for the backup location of your choice above.

**DBBACKUP_SEND_EMAIL (optional)** -
   Controls whether or not django-dbbackup sends an error email when an
   uncaught exception is received. This is ``True`` by default.

**DBBACKUP_DATE_FORMAT (optional)** -
   The Python datetime format to use when generating the backup filename. By
   default this is '%Y-%m-%d-%H%M%S'.

**DBBACKUP_SERVER_NAME (optional)** -
   An optional server name to use when generating the backup filename. This is
   useful to help distinguish between development and production servers. By
   default this value is not used and the servername is not included in the
   generated filename.

**DBBACKUP_FILENAME_TEMPLATE (optional)** -
   The template to use when generating the backup filename. By default this is
   '{databasename}-{servername}-{datetime}.{extension}'. This setting can
   also be made a method which takes the following keyword arguments:

    def backup_filename(databasename, servername, timestamp, extension, wildcard):
        pass

   This allows you to modify the entire format of the filename based on the
   time of day, week, or month.  For example, if you want to take advantage of
   Amazon S3's automatic expiry feature, you need to prefix your backups
   differently based on when you want them to expire.

**DBBACKUP_CLEANUP_KEEP (optional)** -
   The number of backups to keep when specifying the --clean flag. Defaults to
   keeping 10 + the first backup of each month.

**DBBACKUP_GPG_RECIPIENT (optional)** -
   The name of the key that is used for encryption. This setting is only used
   when making a backup with the --encrypt option.

**DBBACKUP_GPG_ALWAYS_TRUST (optional)** -
   Always trust the gpg key (True), or not (False). The default value is False.
   This setting is only used when making a backup with the --encrypt option.

**DBBACKUP_MEDIA_PATH (optional)** -
   The path that will be backed up by the 'backup_media' command. If this option
   is not set, then the MEDIA_ROOT setting is used.


## Encryption Settings ##

You can encrypt a backup with the --encrypt option. The backup is done using gpg.

    python manage.py dbbackup --encrypt

Requirements:

* Install the python package python-gnupg: `pip install python-gnupg`.
* You need gpg key.
* Set the setting 'DBBACKUP_GPG_RECIPIENT' to the name of the gpg key.

**DBBACKUP_GPG_RECIPIENT (required)** -
   Name of the gpg key used for encryption.

**DBBACKUP_GPG_ALWAYS_TRUST (optional)** -
   The encryption of the backup file fails if gpg does not trust the public
   encryption key. The solution is to set the option 'trust-model' to 'always'.
   By default this value is False.  Set this to True to enable this option.

------
    
# COMMON ERRORS #

**ERROR [403] The provided token does not allow this operation**

   Creating an app in Dropbox defaults access to "app_folder" as opposed
   to whole folder. Try changing the setting DBBACKUP_DROPBOX_ACCESS_TYPE
   to 'app_folder'. (Ref: issue #9)
    
**Postgres Backups Keep Prompting for Password**

   Postgres does not allow scripting the password within the commands.  You
   can however create a .pgpass file in your home directory which the command
   line tools will use.  Read more about it here: [http://www.postgresql.org/docs/9.3/static/libpq-pgpass.html](http://www.postgresql.org/docs/9.3/static/libpq-pgpass.html) 
    
    
    
    
