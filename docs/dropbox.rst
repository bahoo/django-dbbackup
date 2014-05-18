Storing backups on Dropbox
==========================

In order to backup to Dropbox, you'll first need to create a Dropbox
Account and set it up to communicate with the Django-DBBackup
application. Don't worry, all instructions are below.

Setup Your Dropbox Account
--------------------------

1. Login to Dropbox and navigate to Developers » MyApps.
   https://www.dropbox.com/developers/start/setup#python

2. Click the button to create a new app and name it whatever you like.
   For reference, I named mine 'Website Backups'.

3. After your app is created, note the options button and more
   importantly the 'App Key' and 'App Secret' values inside. You'll need
   those later.

Setup Your Django Project
-------------------------

1.) Install django-dbbackup and the required Python Dropbox Client API.
If using Pip, you can install this package using the following command:

::

    cd django-dbbackup
    python setup.py install
    pip install dropbox

2.) Add 'dbbackup' to INSTALLED\_APPS in your settings.py file.

3.) Include the required settings below.

::

    DBBACKUP_STORAGE = 'dbbackup.storage.dropbox_storage'
    DBBACKUP_TOKENS_FILEPATH = '<local_tokens_filepath>'
    DBBACKUP_DROPBOX_APP_KEY = '<dropbox_app_key>'
    DBBACKUP_DROPBOX_APP_SECRET = '<dropbox_app_secret>'

4.) Now you're ready to use the backup management commands. The first
time you run a command you'll be prompted to visit a Dropbox URL to
allow DBBackup access to your Dropbox account.
