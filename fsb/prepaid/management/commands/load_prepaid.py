# -*- coding: UTF-8 -*-
#from django.core.management.base import NoArgsCommand
from django.core.management.color import no_style
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from django.utils.datastructures import SortedDict
from fsa.core.utils import CsvData
from fsa.server.models import CsvBase
import datetime, logging
import csv, sys, os
from django.contrib.auth.models import User
from keyedcache import cache_delete
from l10n.models import Country
from livesettings import config_get_group, config_value

log = logging.getLogger('fsb.prepaid.managemment')

import gzip
import zipfile
try:
    import bz2
    has_bz2 = True
except ImportError:
    has_bz2 = False

from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--format_csv', default='', dest='format_csv',
                    help='Format CSV file'),
    )
    help = 'Load Prepaid Card Base ./manage.py load_prepaid --format_csv=1 /fsb/prepaid/fixtures/test.csv'
    args = '[fixture ...]'

    def handle(self, fixture_labels, **options):
        from django.db.models import get_apps
        from django.core import serializers
        from django.db import connection, transaction
        from django.conf import settings
        from fsb.prepaid.models import Prepaid

        format_csv = options.get('format_csv','')

        self.style = no_style()

        verbosity = int(options.get('verbosity', 1))
        show_traceback = options.get('traceback', False)

        # commit is a stealth option - it isn't really useful as
        # a command line option, but it can be useful when invoking
        # loaddata from within another script.
        # If commit=True, loaddata will use its own transaction;
        # if commit=False, the data load SQL will become part of
        # the transaction in place when loaddata was invoked.
        commit = options.get('commit', True)

        # Keep a count of the installed objects and fixtures
        fixture_count = 0
        object_count = 0
        models = set()

        humanize = lambda dirname: dirname and "'%s'" % dirname or 'absolute path'

        # Get a cursor (even though we don't need one yet). This has
        # the side effect of initializing the test database (if
        # it isn't already initialized).
        cursor = connection.cursor()

        if commit:
            transaction.commit_unless_managed()
            transaction.enter_transaction_management()
            transaction.managed(True)

        class SingleZipReader(zipfile.ZipFile):
            def __init__(self, *args, **kwargs):
                zipfile.ZipFile.__init__(self, *args, **kwargs)
                if settings.DEBUG:
                    assert len(self.namelist()) == 1, "Zip-compressed fixtures must contain only one file."
            def read(self):
                return zipfile.ZipFile.read(self, self.namelist()[0])

        compression_types = {
            None:   file,
            'gz':   gzip.GzipFile,
            'zip':  SingleZipReader
        }
        if has_bz2:
            compression_types['bz2'] = bz2.BZ2File

        #cd = CsvData(CsvBase.objects.get(pk=format_csv))
        try:
            csb = CsvBase.objects.get(pk=format_csv)
            cd = CsvData(csb.val)
            log.debug(fixture_labels)
            f = open(fixture_labels, "rt")
            reader = csv.reader(f, delimiter=';', dialect='excel')
            for row in reader:
                try:
                    n = cd.parse(row)
                    objects_in_fixture = Prepaid.objects.add_prepaid(n)
                    log.debug("line: {0} => {1}".format(cd.line_num, row))
                except Exception, e:
                    log.error("line: {0} => {1}".format(cd.line_num, e))
                    pass
            label_found = True
        except Exception, e:
            log.error(e)
        finally:
            f.close()
        if object_count > 0:
            sequence_sql = connection.ops.sequence_reset_sql(self.style, models)
            if sequence_sql:
                if verbosity > 1:
                    print "Resetting sequences"
                for line in sequence_sql:
                    cursor.execute(line)

        if commit:
            transaction.commit()
            transaction.leave_transaction_management()

        if object_count == 0:
            if verbosity > 1:
                print "No fixtures found."
        else:
            if verbosity > 0:
                print "Installed {0} object(s) from {1} fixture(s)".format(object_count, fixture_count)

        # Close the DB connection. This is required as a workaround for an
        # edge case in MySQL: if the same connection is used to
        # create tables, load data, and query, the query can return
        # incorrect results. See Django #7572, MySQL #37735.
        if commit:
            connection.close()
