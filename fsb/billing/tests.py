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
from fsb.billing.models import Balance, CreditBase
from fsa.server.models import Server
#from satchmo_store.contact.models import Contact, ContactRole
from livesettings import ConfigurationSettings, config_value, config_choice_values
from decimal import Decimal
import csv, sys, os

class BaseTestCase(test.TestCase):
    #fixtures = ['testsite', 'alias', 'context', 'extension', 'server', 'acl', 'gateway', 'fsgroup', 'sipprofile', 'testnp', 'testendpoint', 'testcdr', 'currency_base', 'currency', 'tariffplan', 'l10n-data.yaml', 'test-config.yaml', 'test_contact.yaml', 'product_category', 'product']
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'test')
        self.user2 = User.objects.create_user('test2', 'test@test.com', 'test')
        #self.Contact1 = Contact.objects.create(first_name="Jim", last_name="Tester",
        #    role=ContactRole.objects.get(pk='Customer'), email='test@test.com', user=self.user)
        # Every test needs a client.
        self.client = Client()

    def testBalance(self):
        """docstring for billing core"""
        new_balance = Balance.objects.create_balance(self.user)
        #self.assertEquals(new_balance.accountcode.pk, 1)
        #self.assertEquals(new_balance.tariff.pk, 1)
        #self.assertEquals(new_balance.cash, config_value('SHOP','BALANCE_CASH'))
        self.assertEquals(new_balance.cash, Decimal("0.0"))
        new_balance = Balance.objects.get(pk=self.user.pk)
        self.assertEquals(new_balance.cash, Decimal("0.0"))
        new_balance = Balance.objects.create_balance(self.user, '1.33')
        self.assertEquals(new_balance.cash, Decimal("0.0"))

    def testCredit(self):
        bal = Balance.objects.create_balance(self.user)
        self.assertEquals(bal.cash, Decimal("0.0"))
        self.assertEquals(bal.credit, Decimal("0.0"))
        cred = CreditBase(balance=bal, user=self.user2)
        cred.credit=Decimal('10.20')
        cred.enabled=True
        cred.save()
        bal = Balance.objects.get(pk=self.user.pk)
        self.assertEquals(bal.credit, Decimal("10.20"))
        cred.enabled=False
        cred.save()
        bal = Balance.objects.get(pk=self.user.pk)
        self.assertEquals(bal.credit, Decimal("0.0"))

