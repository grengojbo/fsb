# -*- mode: python; coding: utf-8; -*- 
"""
__init__.py

Created by jbo on 2009-08-24.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import logging
log = logging.getLogger('fsadmin.urls') 
from base import urlpatterns as basepatterns
from default import urlpatterns as defaultpatterns
from django.conf.urls.defaults import *
from satchmo_utils import urlhelper
#import satchmo_store

from satchmo_store.shop import get_satchmo_setting
from satchmo_store.shop.views.sitemaps import sitemaps

from fsadmin.urls import urlpatterns

shop_base = get_satchmo_setting('SHOP_BASE')
if shop_base in ('', '/'):
    from satchmo_store.shop.urls import urlpatterns as shoppatterns
else:
    shopregex = '^' + shop_base[1:] + '/'
    shoppatterns = patterns('',
        (shopregex, include('satchmo_store.shop.urls')),
    )

#urlpatterns += basepatterns + defaultpatterns
# TODO исправить кода будет нормально отображатся payment url
urlpatterns += basepatterns + shoppatterns + defaultpatterns
# TODO неправильно удаляет повторы
#urlhelper.remove_duplicate_urls(urlpatterns, [])
