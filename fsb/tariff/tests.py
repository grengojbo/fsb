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
import csv, sys, os
import time, datetime
from decimal import Decimal
from decimal import *
from fsa.core.utils import CsvData
import logging
l = logging.getLogger('fsb.tariff.tests')

class TariffTestCase(test.TestCase):
    #fixtures = ['testsite', 'alias', 'context', 'extension', 'server', 'acl', 'gateway', 'fsgroup', 'sipprofile', 'testnp', 'testendpoint', 'testcdr', 'currency_base', 'currency', 'tariffplan']
    fixtures = ['testsite', 'currency_default', 'test_currency', 'acl', 'alias', 'extension', 'context', 'server', 'server_conf', 'gateway', 'sipprofile', 'tariffplan']
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        
    def testTariffLoad(self):
        """docstring for billing core"""
        from currency.money import Money
        from currency.models import Currency
        from django.contrib.sites.models import RequestSite
        from django.contrib.sites.models import Site
        #tf = TariffPlan.objects.get(enabled=True, primary=True)
        save_cnt = 0
        tariff=1
        site = 1
        format_csv = 1

        #f = open(os.path.join(os.path.dirname(__file__), 'fixtures', '15.csv'), "rt")
        #tf.tariff_format = "delimiter=';'time_format='%d.%m.%Y 00:00'lcr|country_code|special_digits|zeros|name|rate"
        try:
            cd = CsvData("delimiter=';'time_format='%d.%m.%Y 00:00'country_code|name|digits|price|rate|currency|weeks|time_start|time_end")
            f = open(os.path.join(os.path.dirname(__file__), 'fixtures', 'tariff_test.csv'), "rt")
            reader = csv.reader(f, delimiter=';', dialect='excel')
            tf = TariffPlan.objects.get(pk=tariff, enabled=True, site__pk=site)
            for row in reader:
                try:
                    #l.debug(row)
                    country_list, country_code, n = cd.parse(row)
                    l.debug(country_code)
                    for country in country_list:
                        n['country_code'] = country_code
                        digits = n['digits']
                        #price = Money(n['price'], n['currency'])
                        price = Money(n['price'], 'USD')
                        #price = n['price']
                        objects_in_fixture = Tariff.objects.add_tariff(tf, n, digits, price)
                        save_cnt += objects_in_fixture
                        #l.debug(price)
                        #l.debug(n["time_start"])
                        #, n["name"], price )
                        # route
                        #writer.writerow((country_code, n["name"], country, 0, Decimal('0.0000'), Decimal('0.0000'), 1,   Decimal('0.0000'), price, n['brand']))
                        
                except Exception, e:
                    l.error("line: %i => %s" % (cd.line_num, e)) 
                    pass
        finally:
            f.close()
        self.assertEquals(save_cnt, 3)
        res = Tariff.objects.get(digits="38039")
        self.assertEquals(res.country_code, 380)
        self.assertEquals(res.time_start, datetime.time(0, 10))
        self.assertEquals(res.time_end, datetime.time(23, 54))
        self.assertEquals(res.rate, Decimal("0.90"))
        self.assertEquals(res.price, Decimal("0.77"))