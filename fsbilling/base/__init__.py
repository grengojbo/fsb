# -*- mode: python; coding: utf-8; -*-
from userprofile import signals
import logging as l
from fsbilling.base.models import Balance

def handler_create_balance(sender, user, **kwargs):
    l.debug("Signal ProfileRegistration -> handler_create_balance")
    new_balance = Balance.objects.create_balance(user)
    
signals.profile_registration.connect(handler_create_balance)