# -*- mode: python; coding: utf-8; -*- 
from signals_ahoy import signals
#from django import forms
import logging
log = logging.getLogger('fsb.billing.listeners')

def start_listening():
    log.debug('Added billing listeners')
