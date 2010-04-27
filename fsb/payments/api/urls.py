# -*- mode: python; coding: utf-8; -*- 
from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from piston.doc import documentation_view

from fsb.payments.api.handlers import PaymentsHandler
##
auth = HttpBasicAuthentication(realm='FreeSWITCH Admin  API')

payment = Resource(handler=PaymentsHandler, authentication=auth)
##
urlpatterns = patterns('',
    url(r'^$', payment),
    url(r'^doc/$', documentation_view),
    url(r'^query/(?P<transaction_id>.+)/$', payment),
    url(r'^(?P<account>.+)/$', payment),
    #url(r'^posts\.(?P<emitter_format>.+)', blogposts, name='blogposts'),

    # automated documentation
)