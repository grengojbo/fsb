# -*- mode: python; coding: utf-8; -*-
from piston.handler import BaseHandler
#from piston.handler import PaginatedCollectionBaseHandler
from piston.utils import rc, require_mime, require_extended
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from fsa.lcr.models import Lcr
from fsa.gateway.models import SofiaGateway
from fsa.directory.models import Endpoint
from fsb.tariff.models import Tariff
from fsa.core.utils import pars_phone
from threaded_multihost.threadlocals import get_current_user, set_current_user
#from piston.doc import generate_doc
#from fsb.tariff.models import TariffPlan
from django.db import transaction
import keyedcache
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
    def read(self, request, account=None, phone=None, si=None, tariff=None):
        """
        Returns a blogpost, if `title` is given,
        otherwise all the posts.

        Parameters:
         - `phone_number`: The title of the post to retrieve.
        """
        user = request.user
        if user.has_perm("billing.api_view"):
            if phone is not None and si is not None and tariff is not None:
                key_caches_site = "site::{0}".format(si)
                key_caches_tariff = "tariff::{0}::phone::{1}".format(tariff, phone)
                key_caches_phone_site = "phone::{0}::site::{1}".format(phone, si)
                try:
                    resp = keyedcache.cache_get(key_caches_phone_site)
                except:
                    lcr_query = "SELECT l.id AS id, l.digits AS digits, cg.name AS gw, l.rate AS rate, cg.prefix AS gw_prefix, cg.suffix AS suffix, l.price AS price, l.price_currency AS currency, l.name AS name FROM lcr l LEFT JOIN carrier_gateway cg ON l.carrier_id_id=cg.id LEFT JOIN django_site s ON l.site_id=s.id WHERE cg.enabled = '1' AND l.enabled = '1' AND l.digits IN ({0}) AND CURTIME() BETWEEN l.time_start AND l.time_end AND (DAYOFWEEK(NOW()) = l.weeks OR l.weeks = 0) AND s.name='{1}' ORDER BY  digits DESC, reliability DESC, quality DESC;".format(pars_phone(phone), si)
                    log.debug(lcr_query)
                    resp = Lcr.objects.raw(lcr_query)[0]
                    keyedcache.cache_set(key_caches_phone_site, value=resp)
                    #resp = Lcr.objects.phone_lcr(phone, si)
                try:
                    respt = keyedcache.cache_get(key_caches_tariff)
                except:
                    #respt = Tariff.objects.phone_tariff(phone, tariff)
                    query = "select * from tariff where tariff_plan_id=%i AND digits IN (%s) ORDER BY digits DESC, rand();" % (int(tariff), pars_phone(phone))
                    respt = Tariff.objects.raw(query)[0]
                    keyedcache.cache_set(key_caches_tariff, value=respt)
                return {"lcr_rate": resp.rate, "suffix": resp.suffix, "lcr_digits": resp.digits, "lcr_carrier": resp.gw, "lcr_price": resp.price, "lcr_currency": resp.currency, "lcr_name": resp.name, "nibble_rate": respt.rate }
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

class BillingInHandler(BaseHandler):
    allowed_methods = ('GET')
    #model = Endpoint
    fields = ('uid', 'password', 'phone_alias', 'phone_redirect', 'username', 'phone_type',
              ('site', ('name', 'domain')),'effective_caller_id_name','enable', 'is_registered',
              'last_registered', 'sip_server', 'reg_server', 'cidr_ip', 'cidr_mask', 'mac_adress',
              'max_calls', 'zrtp', 'srtp',
              ('accountcode', ('pk', 'username', 'email', 'first_name', 'last_name')))
    #, 'user_context', 'sip_profile'

    def read(self, request, phone=None, gw=None):
        user = request.user
        log.debug('BillingInHandler: {0} {1} {2}'.format(user, phone, gw))
        if user.has_perm("billing.api_view"):
            if phone is not None and gw is not None:
                key_caches_gw = "gatewayw::{0}".format(gw)
                key_caches_endpoint = "endpoint::{0}".format(phone)
                dialplan_caches_gw = "dialplan::gatewayw::{0}::endpoint::{1}".format(gw, phone)
                dialplan_caches_endpoint = "dialplan::endpoint::{0}".format(phone)
                try:
                    gateway = keyedcache.cache_get(key_caches_gw)
                except:
                    gateway = SofiaGateway.objects.get(name__exact=gw, enabled=True)
                    keyedcache.cache_set(key_caches_gw, value=gateway)
                    log.error("Is not gateway: {0}".format(gw))
                #log.debug(gateway.id)
                #lcr_query = "SELECT l.id AS id, l.digits AS digits, l.rate AS rate, l.price AS price, l.price_currency AS currency, l.name AS name FROM lcr l WHERE l.carrier_id_id= '{1}' AND l.enabled = '1' AND l.digits IN ({0}) AND CURTIME() BETWEEN l.time_start AND l.time_end AND (DAYOFWEEK(NOW()) = l.weeks OR l.weeks = 0) ORDER BY  digits DESC, reliability DESC, quality DESC;".format(pars_phone(phone), gateway.id)
                lcr_query = "SELECT l.id AS id, l.digits AS digits, l.rate AS rate, l.price AS price, l.price_currency AS currency, l.name AS name FROM lcr l WHERE l.carrier_id_id= '{1}' AND l.enabled = '1' AND l.digits IN ({0}) ORDER BY  digits DESC, reliability DESC, quality DESC;".format(pars_phone(phone), gateway.id)
                #log.debug(lcr_query)
                #resp = Lcr.objects.raw(lcr_query)[0]
                try:
                    lcr = keyedcache.cache_get(dialplan_caches_gw)
                    lcr_rate = lcr.lcr_rate
                    lcr_price = lcr.lcr_price
                    lcr_currency = lcr.lcr_currency
                except:
                    try:
                        resp = Lcr.objects.raw(lcr_query)[0]
                        lcr_price = resp.price
                        lcr_rate = resp.rate
                        lcr_currency = resp.currency
                        keyedcache.cache_set(dialplan_caches_gw, value={"lcr_rate": lcr_rate, "lcr_price": lcr_price, "lcr_currency": lcr_currency})
                    except:
                        log.error("Is not lcr gateway: {0}".format(gw))
                        lcr_rate = lcr_price = "0.18"
                        lcr_currency = "UAH"
                #endpoint = Endpoint.objects.get(uid__exact=phone, enable=True)
                try:
                    endpoint = keyedcache.cache_get(key_caches_endpoint)
                except:
                    try:
                        endpoint = Endpoint.objects.get(uid__exact=phone, enable=True)
                        keyedcache.cache_set(key_caches_endpoint, value=endpoint)
                    except:
                        endpoint = None
                        keyedcache.cache_set(key_caches_endpoint, value=endpoint)
                #return {"lcr_rate": resp.rate, "suffix": resp.suffix, "lcr_digits": resp.digits, "lcr_carrier": resp.gw, "lcr_price": resp.price, "lcr_currency": resp.currency, "lcr_name": resp.name, "nibble_rate": respt.rate }
                return {"lcr_rate": lcr_rate, "lcr_price": lcr_rate, "lcr_currency": lcr_currency, "endpoint": endpoint}
            else:
                return rc.NOT_HERE
        else:
            return rc.FORBIDDEN
