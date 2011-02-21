# -*- mode: python; coding: utf-8; -*-
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

__author__ = '$Author$'
__revision__ = '$Revision$'

import unittest
from django import test
from django.test.client import Client
from django.contrib.auth.models import User
#from fsb.core.models import c
#from fsa.server.models import Server
from fsb.tariff.models import TariffPlan, Tariff
from bursar.numbers import trunc_decimal
import csv, sys, os
import time, datetime
from decimal import Decimal
from decimal import *
from fsa.core.utils import CsvData
import logging
log = logging.getLogger('fsb.tariff.tests')

class TariffTestCase(test.TestCase):
    #fixtures = ['testsite', 'alias', 'context', 'extension', 'server', 'acl', 'gateway', 'fsgroup', 'sipprofile', 'testnp', 'testendpoint', 'testcdr', 'currency_base', 'currency', 'tariffplan']
    fixtures = ['testsite', 'currency_default', 'test_currency', 'acl', 'alias', 'extension', 'context', 'server', 'server_conf', 'test_gateway', 'sipprofile', 'tariffplan']
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def testTariffLoad(self):
        """docstring for billing core"""
        from currency.money import Money
        #from currency.models import Currency
        #from django.contrib.sites.models import RequestSite
        from django.contrib.sites.models import Site

        f = open(os.path.join(os.path.dirname(__file__), 'fixtures', 'tariff_test.csv'), "rt")
        #tf = TariffPlan.objects.get(enabled=True, primary=True)
        save_cnt = 0
        tariff=1
        site = 1
        format_csv = 1
        fixture_count = 0
        object_count = 0

        try:
            cd = CsvData("delimiter=';'time_format='%d.%m.%Y'country_code|operator_type|name|pref_digits|price|rate|currency|weeks|time_start|time_end|date_start|time_round|code")
            reader = csv.reader(f, delimiter=';', dialect='excel')
            tf = TariffPlan.objects.get(pk=tariff, enabled=True, site__pk=site)
            s = Site.objects.get(pk=site)
            for row in reader:
                try:
                    country_list, country_code, n = cd.parse(row)
                    log.debug("country_code {0} ({1})".format(country_code, country_list))
                    for country in country_list:
                        n['country_code'] = country_code
                        digits = country
                        price = n['price']
                        log.debug("digits {0}".format(country))
                        if n['weeks'] is not None:
                            if n['weeks'] == "all":
                                n['week'] = 0
                                objects_in_fixture = Tariff.objects.add_tariff(tf, n, country, price)
                                object_count += objects_in_fixture
                            else:
                                for i in eval(n['weeks']):
                                    n['week'] = int(i)
                                    objects_in_fixture = Tariff.objects.add_tariff(tf, n, country, price)
                                    object_count += objects_in_fixture
                except Exception, e:
                    log.error("line: {0} => {1}".format(cd.line_num, e))
                    pass
            label_found = True
        except Exception, e:
            log.error(e)
        finally:
            f.close()
        self.assertEquals(object_count, 16)
        key_caches_tariff = "tariff::{0}".format(tariff)
        try:
            res = keyedcache.cache_get(key_caches_tariff)
        except:
            pass
        res = Tariff.objects.get(digits="38094")
        self.assertEquals(res.country_code, 380)
        self.assertEquals(res.time_start, datetime.time(0, 10))
        self.assertEquals(res.time_end, datetime.time(23, 54))
        self.assertEquals(res.rate, Decimal("0.96"))
        self.assertEquals(res.price, Decimal("0.80"))
