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
#from fsbilling.core.models import c
from fsadmin.server.models import Server
from fsbilling.tariff.models import TariffPlan, Tariff
import csv, sys, os

class TariffTestCase(test.TestCase):
    fixtures = ['testsite', 'alias', 'context', 'extension', 'server', 'acl', 'gateway', 'fsgroup', 'sipprofile', 'testnp', 'testendpoint', 'testcdr', 'currency_base', 'currency', 'tariffplan']
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        
    def testTariffLoad(self):
        """docstring for billing core"""
        tf = TariffPlan.objects.get(enabled=True, primary=True)

        f = open(os.path.join(os.path.dirname(__file__), 'fixtures', '15.csv'), "rt")
        tf.tariff_format = "delimiter=';'time_format='%d.%m.%Y 00:00'lcr|country_code|special_digits|zeros|name|rate"
        try:
            res = Tariff.objects.load_tariff(tf, f)
            self.assertEquals(res, 286) 
        finally:
            f.close()
        f = open(os.path.join(os.path.dirname(__file__), 'fixtures', '14.csv'), "rt")
        tf.tariff_format = "delimiter=';'time_format='%d.%m.%Y 00:00'lcr|special_digits|zeros|name|rate"
        try:
            res = Tariff.objects.load_tariff(tf, f)
            self.assertEquals(res, 577) 
        finally:
            f.close()