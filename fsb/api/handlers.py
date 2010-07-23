# -*- mode: python; coding: utf-8; -*-
from piston.handler import BaseHandler
#from piston.handler import PaginatedCollectionBaseHandler
from piston.utils import rc, require_mime, require_extended
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from threaded_multihost.threadlocals import get_current_user, set_current_user
#from piston.doc import generate_doc
#from fsb.tariff.models import TariffPlan
from django.db import transaction

import logging

log = logging.getLogger('fsb.api.handlers')
#from fsb.billing.models import Balance

class BillingHandler(BaseHandler):
    """
    Authenticated entrypoint for blogposts.
    """
    allowed_methods = ('GET')
    #allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    #model = Balance
    #fields = (('accountcode', ('username', 'email', 'first_name', 'last_name', 'date_joined', 'last_registered')), 'cash', ('tariff', ('id', 'name')),'enabled')

    #@staticmethod
    #def resource_uri():
    #    return ('api_numberplan_handler', ['phone_number'])
    
    #@require_mime('json')
    def read(self, request, account=None):
        """
        Returns a blogpost, if `title` is given,
        otherwise all the posts.

        Parameters:
         - `phone_number`: The title of the post to retrieve.
        """
        user = get_current_user()
        if user.has_perm("billing.api_view"):
            return {"rate": 1}
        else:
            rc.FORBIDDEN
        #s = Site.objects.get(name__iexact=request.user)
        #self.resource_name = 'bill'
        #try:
            #if account is not None:
                #log.debug("read accounts %s" % account)
                #return {"count": 1, "accounts": Balance.objects.get(accountcode__username__exact=account, site__name__exact=request.user)}
            #else:
                ##resp = base.filter(site__name__iexact=request.user)[start:limit]
                ##count = base.filter(site__name__iexact=request.user).count()
                ##return {"count": count, "accounts": resp}
                #self.resources = Balance.objects.filter(site__name__exact=request.user)
                #return super(AccountHandler, self).read(request)
        #except:
            #return rc.NOT_HERE
