# -*- mode: python; coding: utf-8; -*-
from decimal import Decimal
from django.contrib.sites.models import Site
from django.test import TestCase
from keyedcache import cache_delete
from l10n.models import Country
from livesettings import config_get_group, config_value
from models import *
from product.models import Product
from satchmo_store.contact.models import AddressBook, Contact, ContactRole
from satchmo_store.shop.models import Order, OrderItem, OrderItemDetail
#from utils import generate_certificate_code, generate_code
from fsbilling.base.models import CurrencyBase
import datetime, logging
import csv, sys, os

log = logging.getLogger('prepaid.tests')

def make_test_order(country, state):
    c = Contact(first_name="Prepaid", last_name="Tester", 
        role=ContactRole.objects.get(pk='Customer'), email="prepaid@example.com")
    c.save()
    if not isinstance(country, Country):
        country = Country.objects.get(iso2_code__iexact = country)
    ad = AddressBook(contact=c, description="home",
        street1 = "test", state=state, city="Portland",
        country = country, is_default_shipping=True,
        is_default_billing=True)
    ad.save()
    site = Site.objects.get_current()
    o = Order(contact=c, shipping_cost=Decimal('0.00'), site=site)
    o.save()

    p = Product.objects.get(slug='GIFT10')
    price = p.unit_price
    log.debug("creating with price: %s", price)
    item1 = OrderItem(order=o, product=p, quantity='2.0',
        unit_price=price, line_item_price=price*2)
    item1.save()

    detl = OrderItemDetail(name = 'email', value='me@example.com', sort_order=0, item=item1)
    detl.save()
    detl = OrderItemDetail(name = 'message', value='hello there', sort_order=0, item=item1)
    detl.save()

    return o

class TestCertCreate(TestCase):
    fixtures = ['testsite', 'alias', 'context', 'extension', 'server', 'acl', 'gateway', 'fsgroup', 'sipprofile', 'testnp', 'testendpoint', 'testcdr', 'currency_base', 'currency', 'tariffplan', 'l10n-data.yaml', 'test-config.yaml', 'test_contact.yaml']
    
    def setUp(self):
        self.site = Site.objects.get_current()
    
    def tearDown(self):
        cache_delete()

    def testCreate(self):
        c = CurrencyBase.objects.get(code='GRN')
        f = open(os.path.join(os.path.dirname(__file__), 'fixtures', 'test.csv'), "rt")
        try:
            res = Prepaid.objects.load_prepaid(c, self.site, f)
            self.assertEquals(res, 3) 
        finally:
            f.close()
        #gc = GiftCertificate(start_balance = '100.00', site=self.site)
        #gc.save()
        
        #self.assert_(gc.code)
        #self.assertEqual(gc.balance, Decimal('100.00'))

    def testUse(self):
        #gc = GiftCertificate(start_balance = '100.00', site=self.site)
        #gc.save()
        #bal = gc.use('10.00')
        #self.assertEqual(bal, Decimal('90.00'))
        #self.assertEqual(gc.usages.count(), 1)
        pass