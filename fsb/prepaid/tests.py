# -*- mode: python; coding: utf-8; -*-
from decimal import Decimal
from django.contrib.sites.models import Site
from django import test
from django.test.client import Client
from django.contrib.auth.models import User
from keyedcache import cache_delete
from l10n.models import Country
from livesettings import config_get_group, config_value
from models import *
from fsa.core.utils import CsvData
#from product.models import Product
#from satchmo_store.contact.models import AddressBook, Contact, ContactRole
#from satchmo_store.shop.models import Order, OrderItem, OrderItemDetail
##from utils import generate_certificate_code, generate_code
import datetime, logging
import csv, sys, os

l = logging.getLogger('fsb.prepaid.tests')

##def make_test_order(country, state):
##    c = Contact(first_name="Prepaid", last_name="Tester", 
##        role=ContactRole.objects.get(pk='Customer'), email="prepaid@example.com")
##    c.save()
##    if not isinstance(country, Country):
##        country = Country.objects.get(iso2_code__iexact = country)
##    ad = AddressBook(contact=c, description="home",
##        street1 = "test", state=state, city="Portland",
##        country = country, is_default_shipping=True,
##        is_default_billing=True)
##    ad.save()
##    site = Site.objects.get_current()
##    o = Order(contact=c, site=site)
##    o.save()
##
##    p = Product.objects.get(slug='prcard25')
##    price = p.unit_price
##    log.debug("creating with price: %s", price)
##    item1 = OrderItem(order=o, product=p, quantity='1.0', unit_price=price, line_item_price=price)
##    item1.save()

    #detl = OrderItemDetail(name = 'email', value='me@example.com', sort_order=0, item=item1)
    #detl.save()
    #detl = OrderItemDetail(name = 'message', value='hello there', sort_order=0, item=item1)
    #detl.save()

    #return o
class TestCertCreate(test.TestCase):
    #fixtures = ['testsite', 'alias', 'server', 'context', 'gateway', 'sipprofile', 'fsgroup', 'testendpoint', 'testcdr', 'acl']
    ##fixtures = ['testsite', 'alias', 'context', 'extension', 'server', 'acl', 'gateway', 'fsgroup', 'sipprofile', 'testnp', 'testendpoint', 'testcdr', 'currency_base', 'currency', 'tariffplan', 'l10n-data.yaml', 'test-config.yaml', 'test_contact.yaml', 'product_category', 'product', 'prepaid', 'test_prepaid']
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.site = Site.objects.get_current()

    def tearDown(self):
        cache_delete()

    def testCreate(self):
        try:
            #f = open(os.path.join(os.path.dirname(__file__), 'fixtures', 'test_all.csv'), "rt")
            f = open(os.path.join(os.path.dirname(__file__), 'fixtures', 'test.csv'), "rt")
            save_cnt = 0
            cd = CsvData("delimiter=';'time_format='%d.%m.%Y 00:00'num_prepaid|code|rate|nt|zeros|date_end")
            reader = csv.reader(f, delimiter=';', dialect='excel')
            for row in reader:
                try:
                    n = cd.parse(row)
                    objects_in_fixture = Prepaid.objects.add_prepaid(n)
                except Exception, e:
                    l.error("line: %i => %s" % (cd.line_num, e)) 
            #objects_in_fixture = Prepaid.objects.load_prepaid(c, site, f)
            label_found = True
        except Exception, e:
            l.error(e)
        finally:
            f.close()
        
        gc = Prepaid.objects.all()
        self.assertEqual(gc.count(),3)
        

##    def testUse(self):
##        #gc = GiftCertificate(start_balance = '100.00', site=self.site)
##        #gc.save()
##        #bal = gc.use('10.00')
##        #self.assertEqual(bal, Decimal('90.00'))
##        #self.assertEqual(gc.usages.count(), 1)
##        pass
##        
##class PrepaidOrderTest(TestCase):
##    fixtures = ['testsite', 'alias', 'context', 'extension', 'server', 'acl', 'gateway', 'fsgroup', 'sipprofile', 'testnp', 'testendpoint', 'testcdr', 'currency_base', 'currency', 'tariffplan', 'l10n-data.yaml', 'test-config.yaml', 'test_contact.yaml', 'product_category', 'product', 'prepaid', 'test_prepaid']
##    def setUp(self):
##        self.site = Site.objects.get_current()
##    
##    def tearDown(self):
##        cache_delete()
##
##    def testOrderSuccess(self):
##        """Test cart creation on order success"""
##        cache_delete()
##        order = make_test_order('US', '')
##        order.order_success()
##    
##        #certs = order.giftcertificates.all()
##        #self.assertEqual(len(certs), 1)
##        #c = certs[0]
##        #self.assertEqual(c.balance, Decimal('20.00'))
##        #self.assertEqual(c.recipient_email, 'me@example.com')
##        #self.assertEqual(c.message, 'hello there')
##    