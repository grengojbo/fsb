# -*- mode: python; coding: utf-8; -*-
"""
base.py

Created by jbo on 2009-08-24.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""
from django.conf.urls.defaults import *
from satchmo_store.shop import get_satchmo_setting
from signals_ahoy.signals import collect_urls
from product.urls.base import adminpatterns as prodpatterns
from shipping.urls import adminpatterns as shippatterns
import logging
import satchmo_store

log = logging.getLogger('fsadmin.urls')

urlpatterns = patterns('',
    (r'^settings/', include('livesettings.urls')),
    (r'^cache/', include('keyedcache.urls')),
) + prodpatterns 
# TODO наверное надо будет включить
#+ shippatterns

collect_urls.send(sender=satchmo_store, patterns=urlpatterns)
