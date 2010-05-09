# -*- mode: python; coding: utf-8; -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list_detail import object_list
#from sugar.views.decorators import render_to
from django.shortcuts import get_object_or_404
#from lib.helpers import reverse
from fsa.server.models import Server, SipProfile, Conf
from fsa.server.config import active_modules
import logging
log = logging.getLogger('fsb.billing.views')

__author__ = '$Author:$'
__revision__ = '$Revision:$'

# Create your views here.

def get_conf(request):
    """return nibblebill config file"""
    log.debug(request.POST.get('hostname')) 
    es = get_object_or_404(Server, name__exact=request.POST.get('hostname'), enabled=True)
    #l.debug("es.odbc_dsn %s" % (es.odbc_dsn))
    return request.Context({'name':request.POST.get('hostname'), 'es':es}).render_response('billing/nibblebill.conf.xml')
