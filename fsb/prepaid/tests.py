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
from fsb.billing.models import Balance, BalanceHistory
from fsa.directory.models import Endpoint
##from utils import generate_certificate_code, generate_code
from fsb.billing.models import BalanceHistory, Balance
from django.db import transaction
from django.db.models import F
from decimal import Decimal
import time, datetime
import md5
import logging
import random
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
        self.user = User.objects.create_user('test', 'test@test.com', 'test')

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
        self.assertEqual(gc.count(),6)
        res = Prepaid.objects.is_valid('11018','222222222')
        self.assertEquals(res.num_prepaid, '11018')
        
        #bal = Balance.objects.get(accountcode=self.user)
        #self.assertEquals(bal.cash, Decimal("25"))
        #res = Prepaid.objects.is_valid('11019','222222222')
        #self.assertEquals(res, None)
        #res = Prepaid.objects.is_valid('11018','111111111')
        #self.assertEquals(res, None)
        
        res = Prepaid.objects.is_valid('11019','111111111')
        self.assertEquals(res.code, '111111111')
        self.assertEquals(res.nt, 1)
        #if res is not None and res.nt == 1:
            #r = res.activate_card(self.user)
        #bal = Balance.objects.get(accountcode=self.user)
        #self.assertEquals(bal.cash, Decimal("75"))
        
        
        
        pay_date = datetime.datetime.now()
        name = 'add:::lincom3000:::prepaid:::{0}'.format(res.pk)
        comments ='Added prepaid card'
        method = 'from site prepaid'
        
        code = "{0}{1}{2}".format(name, comments, method)
        mcode = md5.new()
        mcode.update(code.upper())
        
        temp_txt = "".join([str(random.randint(0, 9)) for i in range(20)])
        pay_transaction_id = "{0}X{1}".format(int(time.time()), temp_txt)
        
        if res is not None and res.nt == 1:
            bal = Balance.objects.get(accountcode__username__exact=self.user.username)
            up_ball = Balance.objects.filter(accountcode=bal).update(cash=F('cash') + res.start_balance)
            r = res.activate_card(bal)
            b = BalanceHistory.objects.create(name = name, accountcode= bal, site = bal.site, pay_date=pay_date,
                method = method, amount = Decimal(res.start_balance), transaction_id = pay_transaction_id,
                details=comments, reason_code=mcode.hexdigest())
            b.save()
        self.assertEquals(r, True)
        bres = BalanceHistory.objects.get(transaction_id__exact=pay_transaction_id)
        self.assertEquals(bres.amount, Decimal("50"))
        result = Balance.objects.get(accountcode__username__exact=self.user.username)
        self.assertEquals(result.cash, Decimal("50"))
        
        
        res = Prepaid.objects.is_valid('11019','111111111')
        self.assertEquals(res, None)
        
        #up_ball = Balance.objects.filter(accountcode=bal).update(cash=F('cash') + res.start_balance)
        #BalanceHistory.objects.create(name=name, accountcode__username__exact=self.user, cash=res.start_balance, comments=comments)
        
        #res = Prepaid.objects.is_valid('5003020','123456781')
        #if res is not None and res.nt == 2:
        #    new_user = User.objects.create_user(res.num_prepaid, '', res.code)
        #    new_endpoint = Endpoint.objects.create_endpoint(new_user, res.num_prepaid)
        #    r = res.activate_card(self.user)
        #self.assertEquals(res.nt, 2)
        #bal = Balance.objects.get(accountcode=new_user)
        
        

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