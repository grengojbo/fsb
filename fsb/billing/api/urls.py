# -*- mode: python; coding: utf-8; -*-
from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
#from piston.doc import documentation_view

from fsb.billing.api.handlers import AccountHandler

auth = HttpBasicAuthentication(realm='FreeSWITCH Admin  API')

account = Resource(handler=AccountHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^$', account, name='account'),
    url(r'^(?P<account>.+)/$', account),
)
