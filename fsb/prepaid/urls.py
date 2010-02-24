# -*- mode: python; coding: utf-8; -*-
from django.conf.urls.defaults import *
from livesettings import config_value, config_get_group

#config = config_get_group('PAYMENT_PREPAID')

urlpatterns = patterns('',
     url(r'^$', 'fsb.prepaid.views.prepaid_form', name='prepaid_view'),
     url(r'^activate/$', 'fsb.prepaid.views.prepaid_form', name='prepaid_activate'),
)
