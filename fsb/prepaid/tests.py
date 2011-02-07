# -*- mode: python; coding: utf-8; -*-
import base64
from django import test
from django.test.client import Client
from keyedcache import cache_delete
import datetime
from decimal import *
from models import *
from fsa.core.utils import CsvData
import base64
import logging
import csv, os
import forms
from django.core import mail
from django.core.urlresolvers import reverse
from fsb.billing.models import Balance, BalanceHistory
from django.contrib.auth.models import Group

l = logging.getLogger('fsb.prepaid.tests')

class TestPrepaid(test.TestCase):

    #urls = 'fsb.prepaid.urls_test'
    #fixtures = ['testsite', 'alias', 'server', 'context', 'gateway', 'sipprofile', 'fsgroup', 'testendpoint', 'testcdr', 'acl']
    ##fixtures = ['testsite', 'alias', 'context', 'extension', 'server', 'acl', 'gateway', 'fsgroup', 'sipprofile', 'testnp', 'testendpoint', 'testcdr', 'currency_base', 'currency', 'tariffplan', 'l10n-data.yaml', 'test-config.yaml', 'test_contact.yaml', 'product_category', 'product', 'prepaid', 'test_prepaid']
    fixtures = ['testsite', 'currency_default', 'test_currency', 'acl', 'alias', 'extension', 'context', 'server', 'server_conf', 'test_gateway', 'sipprofile', 'tariffplan']
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        self.auth_string = 'Basic {0:>s}'.format(base64.encodestring('alice:swordfish').rstrip())
        self.auth_string_error = 'Basic {0:>s}'.format(base64.encodestring('alice:alice').rstrip())
        self.site = Site.objects.get_current()
        self.user = User.objects.create_user('test', 'test@test.com', 'test')
        try:
            #f = open(os.path.join(os.path.dirname(__file__), 'fixtures', 'test_all.csv'), "rt")
            f = open(os.path.join(os.path.dirname(__file__), 'fixtures', 'test_prepaid.csv'), "rt")
            save_cnt = 0
            cd = CsvData("delimiter=';'time_format='%d.%m.%Y'num_prepaid|code|rate|nt|zeros|date_end")
            reader = csv.reader(f, delimiter=';', dialect='excel')
            for row in reader:
                try:
                    n = cd.parse(row)
                    objects_in_fixture = Prepaid.objects.add_prepaid(n)
                except Exception, e:
                    l.error("line: {0} => {1}".format(cd.line_num, e))
            #objects_in_fixture = Prepaid.objects.load_prepaid(c, site, f)
            label_found = True
        except Exception, e:
            l.error(e)
        finally:
            f.close()

    def tearDown(self):
        cache_delete()

    def testPrepaidLoad(self):
        gc = Prepaid.objects.all()
        self.assertEqual(gc.count(),15)
        res= Prepaid.objects.get(num_prepaid__iexact=102)
        self.assertEqual(res.start_balance, Decimal('25'))
        self.assertEqual(res.date_end, datetime.date(2014, 12, 30))

    def testPrepaidForm(self):
        invalid_data_dicts = [
            # Non-numbner.
            {'data': { 'prnumber': 'sdfsfd2',
                    'prcode': '222222222'},
            'error': ('prnumber', [u'This value must contain only letters, numbers and underscores.'])},
            {'data': { 'prnumber': '',
                    'prcode': '222222222'},
            'error': ('prnumber', [u'This field is required.'])},
            {'data': { 'prnumber': '111111',
                    'prcode': '12345678901234567890'},
            'error': ('prcode', [u'Ensure this value has at most 16 characters (it has 20).'])},
            {'data': { 'prnumber': '111111',
                    'prcode': 'sdfgfgdfg'},
            'error': ('prcode', [u'This value must contain only letters, numbers and underscores.'])},
            {'data': { 'prnumber': '111111',
                    'prcode': ''},
            'error': ('prcode', [u'This field is required.'])},
            ]
        for invalid_dict in invalid_data_dicts:
            form = forms.PrepaidForm(data=invalid_dict['data'])
            #form.is_valid()
            self.failIf(form.is_valid())
            #l.debug(form.errors[invalid_dict['error'][0]])
            #l.debug(invalid_dict['error'][1])
            self.assertEqual(form.errors[invalid_dict['error'][0]], invalid_dict['error'][1])

    def testPrepaidStartViewInitial(self):
        #log.debug(reverse('register_prepaid'))
        response = self.client.get(reverse('register_prepaid'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'prepaid/start.html')
        self.failUnless(isinstance(response.context['form'],
                                   forms.PrepaidStartForm))

    def testPrepaidStartView(self):
        response = self.client.post(reverse('register_prepaid'),
                                    data={'prnumber': '123456',
                                          'prcode': '12345678',
                                          'username': 'alice',
                                          'email': 'alice@example.com',
                                          'password1': 'swordfish',
                                          'password2': 'swordfish',
                                           'tos': 'on'})
        self.assertEqual(response.status_code, 200)
        #log.debug("----------> {0}".format(response.context['form']))
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None, errors=u"Incorrect number or the code of the card.")
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(reverse('register_prepaid'),
                                    data={'prnumber': '101',
                                          'prcode': '11111',
                                          'username': 'alice',
                                          'email': 'alice@example.com',
                                          'password1': 'swordfish',
                                          'password2': 'swordfish',
                                           'tos': 'on'})
        self.assertEqual(response.status_code, 200)
        #log.debug("----------> {0}".format(response.context['form']))
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None, errors=u"Incorrect number or the code of the card.")
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(PrepaidLog.objects.count(), 2)
        self.assertEqual(PrepaidLog.objects.filter(st=0).count(), 1)
        self.assertEqual(PrepaidLog.objects.filter(st=2).count(), 1)

        response = self.client.post(reverse('register_prepaid'),
                                    data={'prnumber': '101',
                                          'prcode': '1111',
                                          'username': 'alice',
                                          'email': 'alice@example.com',
                                          'password1': 'swordfish',
                                          'password2': 'swordfish',
                                           'tos': 'on'})
        self.assertEqual(response.status_code, 200)
        #log.debug("----------> {0}".format(response.context['form']))
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None, errors=u"Incorrect number or the code of the card.")
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(PrepaidLog.objects.filter(st=1).count(), 1)

        card01 = Prepaid.objects.get(num_prepaid__iexact=101)
        card01.valid = True
        card01.save()

        card02 = Prepaid.objects.get(num_prepaid__iexact=1002)
        card02.valid = True
        card02.save()

        card03 = Prepaid.objects.get(num_prepaid__iexact=1003)
        card03.valid = True
        card03.save()

        card04 = Prepaid.objects.get(num_prepaid__iexact=1024)
        card04.valid = True
        card04.save()

        self.assertEqual(Prepaid.objects.filter(valid=True).count(), 4)

        response = self.client.post(reverse('register_prepaid'),
                                    data={'prnumber': '101',
                                          'prcode': '1111',
                                          'username': 'alice',
                                          'email': 'alice@example.com',
                                          'password1': 'swordfish',
                                          'password2': 'swordfish',
                                           'tos': 'on'})
        self.assertEqual(response.status_code, 200)
        #log.debug("----------> {0}".format(response.context['form']))
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None, errors=u"Incorrect number or the code of the card.")
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(PrepaidLog.objects.filter(st=6).count(), 1)
        self.assertEqual(PrepaidLog.objects.count(), 4)

        response = self.client.post(reverse('register_prepaid'),
                                    data={'prnumber': '1002',
                                          'prcode': '2001',
                                          'username': '',
                                          'email': 'alice@example.com',
                                          'password1': 'swordfish',
                                          'password2': 'swordfish',
                                           'tos': 'on'})
        self.assertEqual(response.status_code, 200)
        #log.debug("----------> {0}".format(response.context['form']))
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field="username", errors=u"This field is required.")
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(PrepaidLog.objects.count(), 4)

        response = self.client.post(reverse('register_prepaid'),
                                    data={'prnumber': '1002',
                                          'prcode': '2001',
                                          'username': 'test',
                                          'email': 'alice@example.com',
                                          'password1': 'swordfish',
                                          'password2': 'swordfish',
                                          'tos': 'on'})
        self.assertEqual(response.status_code, 200)
        #log.debug("----------> {0}".format(response.context['form']))
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field="username", errors=u"A user with that username already exists.")
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(PrepaidLog.objects.count(), 4)

        response = self.client.post(reverse('register_prepaid'),
                                    data={'prnumber': '1002',
                                        'prcode': '2001',
                                        'username': 'tsfdsfs',
                                        'email': 'alice@example.com',
                                        'password1': 'swordfish',
                                        'password2': 'swor',
                                        'tos': 'on'})
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None, errors=u"The two password fields didn't match.")
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(PrepaidLog.objects.count(), 4)
        self.assertEqual(Prepaid.objects.filter(valid=True, enabled=True).count(), 0)

        Group.objects.create(name='user')
        response = self.client.post(reverse('register_prepaid'),
                                    data={'prnumber': '1002',
                                          'prcode': '2001',
                                          'username': 'alice',
                                          'email': 'alice@example.com',
                                          'password1': 'swordfish',
                                          'password2': 'swordfish'
                                           })
        #log.debug("----------> {0}".format(response.context['form']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(PrepaidLog.objects.count(), 4)
        self.assertEqual(Prepaid.objects.filter(valid=True, enabled=True).count(), 0)
        self.assertEqual(PrepaidLog.objects.filter(st=5).count(), 0)


        response = self.client.post(reverse('register_prepaid'),
                                    data={'prnumber': '1002',
                                          'prcode': '2001',
                                          'username': 'alice',
                                          'email': 'alice@example.com',
                                          'password1': 'swordfish',
                                          'password2': 'swordfish',
                                          'tos': 'on'})
        #log.debug("----------> {0}".format(response.context['form']))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(PrepaidLog.objects.filter(st=5).count(), 1)
        self.assertEqual(PrepaidLog.objects.count(), 5)
        self.assertEqual(Prepaid.objects.filter(valid=True, enabled=True).count(), 1)


        # TEST create user
        data_start={'prnumber': '1002',
                    'prcode': '2001',
                    'username': 'alice',
                    'email': 'alice@example.com',
                    'password1': 'swordfish',
                    'password2': 'swordfish',
                    'tos': 'on'}

        new_user = User.objects.get(username__iexact=data_start.get('username'))
        self.assertEqual(new_user.is_active, True)
        self.assertEqual(new_user.email, 'alice@example.com')

        endpoint = Endpoint.objects.get(uid__exact=data_start.get('prnumber'))
        self.assertEqual(endpoint.enable, True)

        bal = Balance.objects.get(accountcode__username__exact=data_start.get('username'))
        self.assertEquals(bal.cash, Decimal("30"))
        self.assertEquals(bal.site.name, 'test1.example.com')

        self.assertEquals(BalanceHistory.objects.all().count(), 1)

        response = self.client.post(reverse('register_prepaid'),
                                    data={'prnumber': '1002',
                                          'prcode': '2001',
                                          'username': 'alice2',
                                          'email': 'alice2@example.com',
                                          'password1': 'swordfish',
                                          'password2': 'swordfish',
                                           'tos': 'on'})
        self.assertEqual(response.status_code, 200)
        #log.debug("----------> {0}".format(response.context['form']))
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None, errors=u"Incorrect number or the code of the card.")
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(PrepaidLog.objects.filter(st=3).count(), 1)
        self.assertEqual(PrepaidLog.objects.count(), 6)

        #TEST activate prepaid card
        #, HTTP_AUTHORIZATION=self.auth_string
        #response = self.client.post('/api/directory/', {"hostname": self.hostname, "section": "directory", "tag_name": "domain", "key_name": "name", "key_value": self.domainname, "action": "sip_auth", "sip_profile": "internal", "ip": self.hostip, "key": "id", "user": phone, "domain": self.domainname})
        response = self.client.post(reverse('prepaid_activate'),
                                    data={'prnumber': '1002',
                                          'prcode': '2001'},
                                    HTTP_AUTHORIZATION=self.auth_string)
        #log.debug("----------> {0}".format(response))
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None, errors=u"Incorrect number or the code of the card.")
        self.assertEquals(response.status_code, 200)
        self.assertEqual(PrepaidLog.objects.filter(st=3).count(), 2)
        self.assertEqual(PrepaidLog.objects.count(), 7)

        response = self.client.post(reverse('prepaid_activate'),
                                    data={'prnumber': '102',
                                          'prcode': '1112'},
                                    HTTP_AUTHORIZATION=self.auth_string)
        #log.debug("----------> {0}".format(response))
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None, errors=u"Incorrect number or the code of the card.")
        self.assertEquals(response.status_code, 200)
        self.assertEqual(PrepaidLog.objects.filter(st=1).count(), 2)
        self.assertEqual(PrepaidLog.objects.count(), 8)
        self.assertEqual(PrepaidLog.objects.filter(st=0).count(), 1)

        response = self.client.post(reverse('prepaid_activate'),
                                    data={'prnumber': '11102',
                                          'prcode': '1112111'},
                                    HTTP_AUTHORIZATION=self.auth_string)
        #log.debug("----------> {0}".format(response))
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None, errors=u"Incorrect number or the code of the card.")
        self.assertEquals(response.status_code, 200)
        self.assertEqual(PrepaidLog.objects.filter(st=0).count(), 2)
        self.assertEqual(PrepaidLog.objects.count(), 9)

        response = self.client.post(reverse('prepaid_activate'),
                                    data={'prnumber': '101',
                                          'prcode': '1112111'},
                                    HTTP_AUTHORIZATION=self.auth_string)
        #log.debug("----------> {0}".format(response))
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field=None, errors=u"Incorrect number or the code of the card.")
        self.assertEquals(response.status_code, 200)
        self.assertEqual(PrepaidLog.objects.filter(st=2).count(), 2)
        self.assertEqual(PrepaidLog.objects.count(), 10)

        bal = Balance.objects.get(accountcode__username__exact='alice')
        self.assertEquals(bal.cash, Decimal("30"))

        response = self.client.post(reverse('prepaid_activate'),
                                    data={'prnumber': '101',
                                          'prcode': '1111'},
                                    HTTP_AUTHORIZATION=self.auth_string)
        #log.debug("----------> {0}".format(response))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(PrepaidLog.objects.filter(st=5).count(), 2)
        self.assertEqual(PrepaidLog.objects.count(), 11)
        self.assertEqual(Prepaid.objects.filter(valid=True, enabled=True).count(), 2)

        bal = Balance.objects.get(accountcode__username__exact='alice')
        self.assertEquals(bal.cash, Decimal("55"))

        self.assertEqual(PrepaidLog.objects.filter(st=3).count(), 2)
        response = self.client.post(reverse('prepaid_activate'),
                                    data={'prnumber': '101',
                                          'prcode': '1111'},
                                    HTTP_AUTHORIZATION=self.auth_string)
        #log.debug("----------> {0}".format(response))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(PrepaidLog.objects.filter(st=3).count(), 3)
        self.assertEqual(PrepaidLog.objects.count(), 12)
        self.assertEqual(Prepaid.objects.filter(valid=True, enabled=True).count(), 2)
