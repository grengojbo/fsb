# -*- mode: python; coding: utf-8; -*-
"""
default.py

Created by jbo on 2009-08-24.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""
from django.conf import settings
from django.conf.urls.defaults import *
import logging
import satchmo_store

log = logging.getLogger('fsadmin.urls')

urlpatterns = patterns('',
    (r'^billing/', include('fsbilling.base.urls')),
)

