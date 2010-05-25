# -*- mode: python; coding: utf-8; -*- 
from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from piston.doc import documentation_view

from fsb.payments.api.handlers import PaymentsHandler

auth = HttpBasicAuthentication(realm='FreeSWITCH Admin  API')

payment = Resource(handler=PaymentsHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^$', payment, name='payment'),
    url(r'^list/(?P<transaction_id>.+)/$', payment),
    url(r'^query/(?P<start_date>.+)/(?P<end_date>.+)/$', payment),
    url(r'^(?P<account>.+)/$', payment),
 )