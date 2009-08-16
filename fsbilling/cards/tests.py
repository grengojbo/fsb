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
from fsbilling.core.models import c
from fsadmin.server.models import Server
import csv, sys, os

class TariffTestCase(test.TestCase):
    fixtures = ['testsite', 'alias', 'context', 'extension', 'server', 'acl', 'gateway', 'fsgroup', 'sipprofile', 'testnp', 'testendpoint', 'testcdr', 'currency', 'tariffplan']
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        
    def testCoreConf(self):
        """docstring for billing core"""
        pass