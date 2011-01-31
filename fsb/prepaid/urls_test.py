# -*- mode: python; coding: utf-8; -*-
from django.conf.urls.defaults import *
from livesettings import config_value, config_get_group
from django.views.generic.simple import direct_to_template

from registration.views import register
from views import prepaid_start_form
#config = config_get_group('PAYMENT_PREPAID')

urlpatterns = patterns('',
     url(r'^$', 'fsb.prepaid.views.prepaid_form', name='prepaid_view'),
     url(r'^activate/$', 'fsb.prepaid.views.prepaid_form', name='prepaid_activate'),
     url(r'^register/$',
         register,
         {'backend': 'accounts.backends.prepaid.PrepaidBackend', 'success_url': 'profile_overview'},
         name='registration_register_prepaid'),
     url(r'^new/$',
         prepaid_start_form,
         {'template_name':'prepaid/activate.html', 'success_url': 'profile_overview'},
         name='register_prepaid'),
)