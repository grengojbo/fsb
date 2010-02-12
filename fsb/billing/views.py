# -*- mode: python; coding: utf-8; -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from fsadmin.server.models import Server
from django.views.generic.list_detail import object_list
from lib.decorators import render_to
from django.shortcuts import get_object_or_404
import logging
l = logging.getLogger('fsb.billing.views')

__author__ = '$Author:$'
__revision__ = '$Revision:$'

# Create your views here.

@render_to('base/nibblebill.conf.xml')    
def get_conf(request):
    """return nibblebill config file"""
    l.debug(request.POST.get('hostname')) 
    es = get_object_or_404(Server, name=request.POST.get('hostname'))
    return {'es':es}