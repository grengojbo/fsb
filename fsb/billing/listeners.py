# -*- mode: python; coding: utf-8; -*- 
from signals_ahoy import signals
from django.contrib.auth.models import User
import datetime
from fsb.billing.models import Balance
from django.db import models

import logging
log = logging.getLogger('fsb.billing.listeners')

def billing_user_post_save(sender, instance, created, **kwargs):
    """Create Billing for user when User is created."""
    if created:
        Balance.objects.create_balance(instance)
        log.debug("Create user: %s" % instance.username)
        
    
def start_listening():
    models.signals.post_save.connect(billing_user_post_save, sender=User)
    log.debug('Added billing listeners')
