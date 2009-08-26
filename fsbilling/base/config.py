# -*- coding: utf-8 -*-

import os
import urlparse
from decimal import Decimal
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from livesettings import config_register, BooleanValue, StringValue, \
    MultipleStringValue, ConfigurationGroup, PositiveIntegerValue, \
    DecimalValue
    
SHOP_GROUP = ConfigurationGroup('SHOP', _('Satchmo Shop Settings'), ordering=0)

config_register(DecimalValue(
    SHOP_GROUP,
        'BALANCE_CASH',
        description = _('Балан при регистрации'),
        help_text = _("Первоначальный баланс при регистрации нового пользователя например 0.25 у.е."),
        default = Decimal('0.25')
    ))

config_register(PositiveIntegerValue(
    SHOP_GROUP,
        'BALANCE_TARIFF',
        description = _('Тариф по умолчанию'),
        help_text = _("Необходимо обязательно создать тариф в тарифном плане"),
        default = 1
    ))