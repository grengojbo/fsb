from django.conf.urls.defaults import *
from livesettings import config_get_group

config = config_get_group('PAYMENT_PREPAID')

urlpatterns = patterns('',
     (r'^$', 'fsbilling.prepaid.views.pay_ship_info', {'SSL':config.SSL.value}, 'PREPAID_satchmo_checkout-step2'),
     (r'^confirm/$', 'fsbilling.prepaid.views.confirm_info', {'SSL':config.SSL.value}, 'PREPAID_satchmo_checkout-step3'),
     (r'^success/$', 'payment.views.checkout.success', {'SSL':config.SSL.value}, 'PREPAID_satchmo_checkout-success'),
     (r'^balance/$', 'fsbilling.prepaid.views.check_balance', {}, 'satchmo_prepaid_balance'),
)
