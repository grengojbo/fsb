# -*- coding: UTF-8 -*-
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

__author__ = '$Author:$'
__revision__ = '$Revision:$'

#from django.test import TestCase
import unittest
from django import test
from django.test.client import Client
from django.contrib.auth.models import User
#from fsadmin.directory.models import Endpoint, SipRegistration
#from fsadmin.dialplan.models import Context
import logging as l

#class SimpleTest(unittest.TestCase):
class XmlCurlTestCase(test.TestCase):
    # TODO fsadmin + fsbilling
    fixtures = ['testsite', 'alias', 'context', 'extension', 'server', 'acl', 'gateway', 'fsgroup', 'sipprofile', 'testnp', 'testendpoint', 'testcdr', 'currency', 'tariffplan', 'l10n-data.yaml', 'test-config.yaml', 'test_contact.yaml']
    # TODO fsadmin
    #fixtures = ['testsite', 'alias', 'context', 'extension', 'server', 'acl', 'gateway', 'fsgroup', 'sipprofile', 'testnp', 'testendpoint', 'testcdr']
    
    def setUp(self):
        # Every test needs a client.
        #self.user = User.objects.create_user('test', 'test@test.com', 'test')
        #self.hostname = 'test1.example.com'
        #self.hostip = '192.168.51.100'
        #self.domainname = '192.168.51.100'
        #self.xml_context = '<result status="not found" />'
        self.client = Client()
    
    def testRegistration(self):
        from userprofile.models import EmailValidation, Avatar, UserProfileMediaNotFound, GoogleDataAPINotFound, S3BackendNotFound
        
        c = Client()
        e = 'admin@linktel.com.ua'
        r = c.get('/', {})
        self.assertEqual(r.status_code, 200)
        #self.assertEqual(unicode(r.context[-1]['params']), '{}')
        #self.assertEqual(unicode(r.context[-1]['profiles']), '[]')

        r = c.get('/accounts/register/', {})
        self.assertEqual(r.status_code, 200)
        #self.assertEqual(unicode(r.context[-1]['form']), '<tr><th><label for="id_username">Имя пользователя:</label></th><td><input id="id_username" type="text" name="username" maxlength="255" /></td></tr>        <tr><th><label for="id_email">E-mail адрес:</label></th><td><input type="text" name="email" id="id_email" /></td></tr><tr><th><label for="id_password1">Пароль:</label></th><td><input type="password" name="password1" id="id_password1" /></td></tr><tr><th><label for="id_password2">Пароль (ещё раз):</label></th><td><input type="password" name="password2" id="id_password2" /></td></tr>')

        r = c.post('/accounts/register/', {'username': 'testreg','password1': 'ifrfks9','password2': 'ifrfks9','email': e,})
        r = c.get('/accounts/register/complete/', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['params']), '{}')
        self.assertEqual(unicode(r.context[-1]['email_validation_required']), 'True')
        
        k = EmailValidation.objects.get(email=e)
        q = "/accounts/email/validation/%s/" % k.key
        r = c.get(q, {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['successful']), 'True')
