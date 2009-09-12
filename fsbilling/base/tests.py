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
from fsbilling.base.models import Balance
from fsadmin.server.models import Server
from satchmo_store.contact.models import Contact, ContactRole
from livesettings import ConfigurationSettings, config_value, config_choice_values
from decimal import Decimal
import csv, sys, os

class BaseTestCase(test.TestCase):
    fixtures = ['testsite', 'alias', 'context', 'extension', 'server', 'acl', 'gateway', 'fsgroup', 'sipprofile', 'testnp', 'testendpoint', 'testcdr', 'currency_base', 'currency', 'tariffplan', 'l10n-data.yaml', 'test-config.yaml', 'test_contact.yaml', 'product_category', 'product']
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'test')
        self.Contact1 = Contact.objects.create(first_name="Jim", last_name="Tester", 
            role=ContactRole.objects.get(pk='Customer'), email='test@test.com', user=self.user)
        # Every test needs a client.
        self.client = Client()
        
    def testBalance(self):
        """docstring for billing core"""
        new_balance = Balance.objects.create_balance(self.Contact1)
        self.assertEquals(new_balance.accountcode.pk, 1)
        self.assertEquals(new_balance.tariff.pk, 1)
        self.assertEquals(new_balance.cash, config_value('SHOP','BALANCE_CASH'))
        #self.assertEquals(new_balance.cash, Decimal("0.0"))