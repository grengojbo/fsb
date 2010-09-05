# -*- mode: python; coding: utf-8; -*-
from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
#from piston.doc import documentation_view

from fsb.api.handlers import BillingHandler, BillingInHandler

auth = HttpBasicAuthentication(realm='FreeSWITCH Admin  API')

bill = Resource(handler=BillingHandler, authentication=auth)
bill_in = Resource(handler=BillingInHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^$', bill, name='bill'),
    url(r'^out/(?P<si>.+)/(?P<phone>.+)/(?P<tariff>.+)/$', bill),
    url(r'^in/(?P<gw>.+)/(?P<phone>.+)/$', bill_in),
)
