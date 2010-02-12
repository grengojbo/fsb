# -*- mode: python; coding: utf-8; -*- 
"""
fsb_base.py

Created by jbo on 2009-07-28.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

from django import template
from django.conf import settings
from satchmo_store.contact.models import Contact
from fsb.billing.models import Balance
from livesettings import config_value
import sys
import logging

l = logging.getLogger('fsb.billing.tags')

register = template.Library()

@register.inclusion_tag('base/balance.html', takes_context=True)
def account_balance(context):
    """docstring for accaut_balance"""
    request = context['request']
    try:
        contact = Contact.objects.from_request(request, create=False)
        balance = Balance.objects.get(accountcode=contact)
    except Contact.DoesNotExist:
        contact = None
        balance = None
    return {'contact' : contact, 'balance' : balance, 'c' : config_value('LANGUAGE', 'CURRENCY')}