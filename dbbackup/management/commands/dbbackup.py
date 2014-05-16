"""
Save backup files to Dropbox.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import re
import datetime
import tempfile
import gzip
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.base import LabelCommand
from optparse import make_option
from ... import utils
from ...dbcommands import DBCommands
from ...dbcommands import DATE_FORMAT
from ...storage.base import BaseStorage
from ...storage.base import StorageError


class Command(LabelCommand):
    help = "dbbackup [-c] [-d <dbname>] [-s <servername>] [--compress] [--encrypt]"
    option_list = BaseCommand.option_list + (
        make_option("-c", "--clean", help="Clean up old backup files", action="store_true", default=False),
        make_option("-d", "--database", help="Database to backup (default: everything)"),
        make_option("-s", "--servername", help="Specifiy server name to include in backup filename"),
        make_option("-z", "--compress", help="Compress the backup files", action="store_true", default=False),
        make_option("-e", "--encrypt", help="Encrypt the backup files", action="store_true", default=False),
    )

    @utils.email_uncaught_exception
    def handle(self, **options):
        """ Django command handler. """
        try:
            self.clean = options.get('clean')
            self.clean_keep = getattr(settings, 'DBBACKUP_CLEANUP_KEEP', 10)
            self.database = options.get('database')
            self.servername = options.get('servername')
            self.filename = options.get('output-file')
            self.compress = options.get('compress')
            self.encrypt = options.get('encrypt')
            self.storage = BaseStorage.storage_factory()
            if self.database:
                database_keys = self.database,
            else:
                database_keys = getattr(settings, 'DBBACKUP_DATABASES', list(settings.DATABASES.keys()))
            for database_key in database_keys:
                database = settings.DATABASES[database_key]
                self.dbcommands = DBCommands(database)
                self.save_new_backup(database, database_key)
                self.cleanup_old_backups(database)
        except StorageError as err:
            raise CommandError(err)

    def save_new_backup(self, database, database_name):
        """ Save a new backup file. """
        print("Backing Up Database: %s" % database['NAME'])
        filename = database_name + ".backup"
        outputfile = tempfile.SpooledTemporaryFile(max_size=10 * 1024 * 1024)
        #outputfile.name = self.dbcommands.filename(self.servername)
        self.dbcommands.run_backup_commands(outputfile)
        if self.compress:
            compressed_file = self.compress_file(outputfile)
            outputfile.close()
            outputfile = compressed_file
        if self.encrypt:
            encrypted_file = utils.encrypt_file(outputfile)
            outputfile = encrypted_file
        print("  Backup tempfile created: %s" % (utils.handle_size(outputfile)))
        print("  Writing file to %s: /%s, filename: %s" % (self.storage.name, self.storage.backup_dir(), filename))
        self.storage.write_file(outputfile, filename)

    def cleanup_old_backups(self, database):
        """ Cleanup old backups, keeping the number of backups specified by
            DBBACKUP_CLEANUP_KEEP and any backups that occur on first of the month.
        """
        if self.clean:
            print("Cleaning Old Backups for: %s" % database['NAME'])
            filepaths = self.storage.list_directory()
            filepaths = self.dbcommands.filter_filepaths(filepaths)
            for filepath in sorted(filepaths[0:-self.clean_keep]):
                regex = r'^%s' % self.dbcommands.filename_match(self.servername, '(.*?)')
                datestr = re.findall(regex, filepath)[0]
                dateTime = datetime.datetime.strptime(datestr, DATE_FORMAT)
                if int(dateTime.strftime("%d")) != 1:
                    print("  Deleting: %s" % filepath)
                    self.storage.delete_file(filepath)

    def compress_file(self, inputfile):
        """ Compress this file using gzip.
            The input and the output are filelike objects.
        """
        outputfile = tempfile.SpooledTemporaryFile(max_size=10 * 1024 * 1024)
        outputfile.name = inputfile.name + '.gz'
        zipfile = gzip.GzipFile(fileobj=outputfile, mode="wb")
        try:
            inputfile.seek(0)
            zipfile.write(inputfile.read())
        finally:
            zipfile.close()
        return outputfile
