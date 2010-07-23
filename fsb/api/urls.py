# -*- mode: python; coding: utf-8; -*- 
from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
#from piston.doc import documentation_view

from fsb.api.handlers import BillingHandler

auth = HttpBasicAuthentication(realm='FreeSWITCH Admin  API')

bill = Resource(handler=BillingHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^$', bill, name='bill'),
    url(r'^(?P<account>.+)/$', bill),
)