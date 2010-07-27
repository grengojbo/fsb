# -*- mode: python; coding: utf-8; -*-
from piston.handler import BaseHandler
#from piston.handler import PaginatedCollectionBaseHandler
from piston.utils import rc, require_mime, require_extended
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from fsa.lcr.models import Lcr
from fsa.core.utils import pars_phone
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
    def read(self, request, account=None, phone=None, si=None):
        """
        Returns a blogpost, if `title` is given,
        otherwise all the posts.

        Parameters:
         - `phone_number`: The title of the post to retrieve.
        """
        user = request.user
        if user.has_perm("billing.api_view"):
            if phone is not None and si is not None:
                lcr_query = "SELECT l.id AS id, l.digits AS digits, cg.name AS gw, l.rate AS rate, cg.prefix AS gw_prefix, cg.suffix AS suffix, l.price AS price, l.price_currency AS currency, l.name AS name FROM lcr l LEFT JOIN carrier_gateway cg ON l.carrier_id_id=cg.id LEFT JOIN django_site s ON l.site_id=s.id WHERE cg.enabled = '1' AND l.enabled = '1' AND l.digits IN ({0}) AND CURTIME() BETWEEN l.time_start AND l.time_end AND (DAYOFWEEK(NOW()) = l.weeks OR l.weeks = 0) AND s.name='{1}' ORDER BY  digits DESC, reliability DESC, quality DESC;".format(pars_phone(phone), si)
                log.debug(lcr_query)
                resp = Lcr.objects.raw(lcr_query)[0]
                return {"lcr_rate": resp.rate, "suffix": resp.suffix, "lcr_digits": resp.digits, "lcr_carrier": resp.gw, "lcr_price": resp.price, "lcr_currency": resp.currency, "lcr_name": resp.name }
            else:
                return rc.NOT_HERE
        else:
            return rc.FORBIDDEN
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
