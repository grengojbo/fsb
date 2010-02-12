# -*- coding: utf-8 -*-

import os
import urlparse
from decimal import Decimal
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from livesettings import config_register, BooleanValue, StringValue, \
    MultipleStringValue, ConfigurationGroup, PositiveIntegerValue, \
    DecimalValue
    
BILLING_GROUP = ConfigurationGroup('BILLING', _('Billing Settings'), ordering=0)

config_register(DecimalValue(
    BILLING_GROUP,
        'BALANCE_CASH',
        description = _('Beginning balance'),
        help_text = _("The initial balance in the new user registration such as 0.25 USD"),
        default = Decimal('0.25')
    ))

config_register(PositiveIntegerValue(
    BILLING_GROUP,
        'BALANCE_TARIFF',
        description = _('Default tariff'),
        help_text = _("Make sure to create a tariff in the tariff plan"),
        default = 1
    ))