# -*- mode: python; coding: utf-8; -*-
from userprofile import signals
import logging
from fsbilling.base.models import Balance

l = logging.getLogger('fsbilling.base') 

def handler_create_balance(sender, contact, **kwargs):
    l.debug("Signal satchmo_registration_verified -> handler_create_balance")
    new_balance = Balance.objects.create_balance(contact)
    
signals.satchmo_registration_verified.connect(handler_create_balance)