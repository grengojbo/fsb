# -*- mode: python; coding: utf-8; -*-
from django.conf.urls.defaults import *
from livesettings import config_value, config_get_group

#config = config_get_group('PAYMENT_PREPAID')

urlpatterns = patterns('',
     #(r'^$', 'fsb.prepaid.views.pay_ship_info', {'SSL':config.SSL.value}, 'PREPAID_satchmo_checkout-step2'),
     #(r'^confirm/$', 'fsb.prepaid.views.confirm_info', {'SSL':config.SSL.value}, 'PREPAID_satchmo_checkout-step3'),
     #(r'^success/$', 'payment.views.checkout.success', {'SSL':config.SSL.value}, 'PREPAID_satchmo_checkout-success'),
     #(r'^balance/$', 'fsb.prepaid.views.check_balance', {}, 'satchmo_prepaid_balance'),
)
