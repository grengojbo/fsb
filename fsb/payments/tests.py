# -*- mode: python; coding: utf-8; -*-
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

# Decimal("7.32").quantize(Decimal('.01'), rounding=ROUND_UP)
"""

__author__ = '$Author$'
__revision__ = '$Revision$'

import unittest
from django import test
from django.test.client import Client
from django.contrib.auth.models import User
from fsb.billing.models import Balance
from fsa.server.models import Server
#from satchmo_store.contact.models import Contact, ContactRole
from livesettings import ConfigurationSettings, config_value, config_choice_values
from decimal import Decimal
from django.contrib.sites.models import Site
import csv, sys, os
import random
from fsb.billing.models import BalanceHistory, Balance
from django.db import transaction
from django.db.models import F
from django.db import models
import logging
import time, datetime

log = logging.getLogger('fsb.payments.tests')

class BaseTestCase(test.TestCase):
    fixtures = ['testsite', 'currency_default', 'test_currency', 'acl', 'alias', 'extension', 'context', 'server', 'server_conf', 'gateway', 'sipprofile', 'tariffplan']
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'test')
        #self.Contact1 = Contact.objects.create(first_name="Jim", last_name="Tester", 
        #    role=ContactRole.objects.get(pk='Customer'), email='test@test.com', user=self.user)
        # Every test needs a client.
        self.client = Client()
        self.pay_date = datetime.datetime.now()
        
    @transaction.commit_manually
    def test01Balance(self):
        """docstring for billing core"""

        new_balance = Balance.objects.create_balance(self.user)
        #self.assertEquals(new_balance.accountcode.pk, 1)
        #self.assertEquals(new_balance.tariff.pk, 1)
        #self.assertEquals(new_balance.cash, config_value('SHOP','BALANCE_CASH'))
        self.assertEquals(new_balance.site, Site.objects.get(name='test1.example.com'))
        self.assertEquals(new_balance.cash, Decimal("0.0"))

        #accountcode = User.objects.get(username__iexact=self.user.username, balance__site__name__iexact='test1.example.com')
        tr = "test{0}".format(random.randrange(1,100))
        amount = '20.10'
        bal = Balance.objects.from_api_get(self.user.username, 'test1.example.com')
        self.assertEquals(bal.accountcode.username, self.user.username)
        paymentargs = {
                "accountcode": bal,
                "name": "add money",
                "site": Site.objects.get(name='test1.example.com'),
                "method": 'from api payments',
                "transaction_id": tr,
                "pay_date": self.pay_date,
                "details":'details ',
            }
        b = BalanceHistory.objects.create_linked(paymentargs, 'test1.example.com', self.user.username, amount)
        self.assertEquals(b.amount, Decimal(amount))
        try:
            
            transaction.commit()
            bal.cash_add(b.amount)
            if bal.is_positiv:
                bal.save()
                b.success = True
                b.save()
##        except BalanceHistory.IntegrityError:
##            log.error("column transaction_id is not unique")
##            transaction.rollback()
        except:
            transaction.rollback()
        else:
            transaction.commit()
        res = Balance.objects.from_api_get(self.user.username, 'test1.example.com')
        self.assertEquals(res.cash, Decimal("20.10"))
        br = BalanceHistory.objects.get(transaction_id=tr)
        self.assertEquals(br.amount, Decimal(amount))
        #self.assertEquals(br.site, 'test.example.com')
        self.assertEquals(br.success, True)
        
    @transaction.commit_manually
    def test02BalanceFalse(self):
        """docstring for billing core"""

        new_balance = Balance.objects.create_balance(self.user)
        #self.assertEquals(new_balance.accountcode.pk, 1)
        #self.assertEquals(new_balance.tariff.pk, 1)
        #self.assertEquals(new_balance.cash, config_value('SHOP','BALANCE_CASH'))
        self.assertEquals(new_balance.site, Site.objects.get(name='test1.example.com'))
        self.assertEquals(new_balance.cash, Decimal("0.0"))

        #accountcode = User.objects.get(username__iexact=self.user.username, balance__site__name__iexact='test1.example.com')
        tr = "test{0}".format(random.randrange(1,100))
        amount = '20.10'
        try:
            bal = Balance.objects.from_api_get(self.user.username, 'test1.example.com')
            self.assertEquals(bal.accountcode.username, self.user.username)
            paymentargs = {
                "accountcode": bal,
                "name": "add money",
                "site": Site.objects.get(name='test1.example.com'),
                "method": 'from api payments',
                "transaction_id": tr,
                "pay_date": self.pay_date,
                "details": 'details ',
            } 
        except Balance.DoesNotExist:
            log.error("DoesNotExist")
        except Site.DoesNotExist:
            log.error("DoesNotExist")
        try:
            b = BalanceHistory.objects.create_linked(paymentargs, 'test1.example.com', self.user.username, amount)
            b = BalanceHistory.objects.create_linked(paymentargs, 'test1.example.com', self.user.username, amount)
            self.assertEquals(b.amount, Decimal(amount))
            transaction.commit()
            bal.cash += b.amount
            if bal.is_positiv:
                bal.save()
                b.success = True
                b.save()
##        except BalanceHistory.IntegrityError:
##            log.error("column transaction_id is not unique")
##            transaction.rollback()
        except:
            transaction.rollback()
        else:
            transaction.commit()
        res = Balance.objects.from_api_get(self.user.username, 'test1.example.com')
        self.assertEquals(res.cash, Decimal("0.0"))
        br = BalanceHistory.objects.get(transaction_id=tr)
        self.assertEquals(br.amount, Decimal(amount))
        #self.assertEquals(br.site, 'test.example.com')
        self.assertEquals(br.success, False)

    @transaction.commit_manually
    def test03BalanceDelete(self):
        """docstring for billing core"""

        new_balance = Balance.objects.create_balance(self.user)
        #self.assertEquals(new_balance.accountcode.pk, 1)
        #self.assertEquals(new_balance.tariff.pk, 1)
        #self.assertEquals(new_balance.cash, config_value('SHOP','BALANCE_CASH'))
        self.assertEquals(new_balance.site, Site.objects.get(name='test1.example.com'))
        self.assertEquals(new_balance.cash, Decimal("0.0"))

        #accountcode = User.objects.get(username__iexact=self.user.username, balance__site__name__iexact='test1.example.com')
        tr = "test{0}".format(random.randrange(1,100))
        amount = '20.10'
        try:
            bal = Balance.objects.from_api_get(self.user.username, 'test1.example.com')
            self.assertEquals(bal.accountcode.username, self.user.username)
            paymentargs = {
                "accountcode": bal,
                "name": "add money",
                "site": Site.objects.get(name='test1.example.com'),
                "method": 'from api payments',
                "transaction_id": tr,
                "pay_date": self.pay_date,
                "details": 'details ',
            } 
        except Balance.DoesNotExist:
            log.error("DoesNotExist")
        except Site.DoesNotExist:
            log.error("DoesNotExist")
        try:
            b = BalanceHistory.objects.create_linked(paymentargs, 'test1.example.com', self.user.username, amount)
            self.assertEquals(b.amount, Decimal(amount))
            transaction.commit()
            bal.cash += b.amount
            if bal.is_positiv:
                bal.save()
                b.success = True
                b.save()
##        except BalanceHistory.IntegrityError:
##            log.error("column transaction_id is not unique")
##            transaction.rollback()
        except:
            transaction.rollback()
        else:
            transaction.commit()
        tr = "test{0}".format(random.randrange(1,100))
        paymentargs = {
                "accountcode": bal,
                "name": "add money",
                "site": Site.objects.get(name='test1.example.com'),
                "method": 'from api payments',
                "transaction_id": tr,
                "pay_date": self.pay_date,
                "details": 'details ',
            }
        amount = '20.05'
        try:
            b = BalanceHistory.objects.create_linked(paymentargs, 'test1.example.com', self.user.username, amount)
            self.assertEquals(b.amount, Decimal(amount))
            transaction.commit()
            bal.cash -= b.amount
            if bal.is_positiv:
                bal.save()
                b.success = True
                b.save()
##        except BalanceHistory.IntegrityError:
##            log.error("column transaction_id is not unique")
##            transaction.rollback()
        except:
            transaction.rollback()
        else:
            transaction.commit()
        res = Balance.objects.from_api_get(self.user.username, 'test1.example.com')
        self.assertEquals(res.cash, Decimal("0.05"))
        br = BalanceHistory.objects.get(transaction_id=tr)
        self.assertEquals(br.amount, Decimal(amount))
        #self.assertEquals(br.site, 'test.example.com')
        self.assertEquals(br.success, True)

    @transaction.commit_manually
    def test04BalanceDeleteFalse(self):
        """docstring for billing core"""

        new_balance = Balance.objects.create_balance(self.user)
        #self.assertEquals(new_balance.accountcode.pk, 1)
        #self.assertEquals(new_balance.tariff.pk, 1)
        #self.assertEquals(new_balance.cash, config_value('SHOP','BALANCE_CASH'))
        self.assertEquals(new_balance.site, Site.objects.get(name='test1.example.com'))
        self.assertEquals(new_balance.cash, Decimal("0.0"))

        #accountcode = User.objects.get(username__iexact=self.user.username, balance__site__name__iexact='test1.example.com')
        tr = "test{0}".format(random.randrange(1,100))
        amount = '20.10'
        try:
            bal = Balance.objects.from_api_get(self.user.username, 'test1.example.com')
            self.assertEquals(bal.accountcode.username, self.user.username)
            paymentargs = {
                "accountcode": bal,
                "name": "add money",
                "site": Site.objects.get(name='test1.example.com'),
                "method": 'from api payments',
                "transaction_id": tr,
                "pay_date": self.pay_date,
                "details": 'details ',
            } 
        except Balance.DoesNotExist:
            log.error("DoesNotExist")
        except Site.DoesNotExist:
            log.error("DoesNotExist")
        try:
            b = BalanceHistory.objects.create_linked(paymentargs, 'test1.example.com', self.user.username, amount)
            self.assertEquals(b.amount, Decimal(amount))
            transaction.commit()
            bal.cash += b.amount
            if bal.is_positiv:
                bal.save()
                b.success = True
                b.save()
##        except BalanceHistory.IntegrityError:
##            log.error("column transaction_id is not unique")
##            transaction.rollback()
        except:
            transaction.rollback()
        else:
            transaction.commit()
        tr = "test{0}".format(random.randrange(1,100))
        paymentargs = {
                "accountcode": bal,
                "name": "add money",
                "site": Site.objects.get(name='test1.example.com'),
                "method": 'from api payments',
                "transaction_id": tr,
                "pay_date": self.pay_date,
                "details": 'details ',
            }
        amount = '-20.15'
        try:
            b = BalanceHistory.objects.create_linked(paymentargs, 'test1.example.com', self.user.username, amount)
            self.assertEquals(b.amount, Decimal(amount))
            transaction.commit()
            bal.cash_del(b.amount)
            if bal.is_positiv:
                bal.save()
                b.success = True
                b.save()
##        except BalanceHistory.IntegrityError:
##            log.error("column transaction_id is not unique")
##            transaction.rollback()
        except:
            transaction.rollback()
        else:
            transaction.commit()
        res = Balance.objects.from_api_get(self.user.username, 'test1.example.com')
        self.assertEquals(res.cash, Decimal("20.10"))
        br = BalanceHistory.objects.get(transaction_id=tr)
        self.assertEquals(br.amount, Decimal(amount))
        #self.assertEquals(br.site, 'test.example.com')
        self.assertEquals(br.success, False)
