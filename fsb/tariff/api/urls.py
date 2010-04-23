# -*- mode: python; coding: utf-8; -*- 
from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from piston.doc import documentation_view

from fsb.tariff.api.handlers import TariffHandler, TariffPlanHandler
##
auth = HttpBasicAuthentication(realm='FreeSWITCH Admin  API')

tariff = Resource(handler=TariffHandler, authentication=auth)
tariffplan = Resource(handler=TariffPlanHandler, authentication=auth)
##
urlpatterns = patterns('',
    url(r'^$', tariffplan),
    url(r'^doc/$', documentation_view),
    url(r'^plan/(?P<tariff>.+)/$', tariffplan),
    url(r'^list/(?P<tariff>.+)/$', tariff),
    url(r'^(?P<tariff>.+)/(?P<phone>.+)/$', tariff),
    #url(r'^posts\.(?P<emitter_format>.+)', blogposts, name='blogposts'),

    # automated documentation
)