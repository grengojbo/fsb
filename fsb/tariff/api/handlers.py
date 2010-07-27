# -*- mode: python; coding: utf-8; -*- 
from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc, require_mime, require_extended
#from piston.doc import generate_doc
import logging
log = logging.getLogger('fsb.tariff.api.handlers')
#from fsa.directory.models import Endpoint
#from fsa.numberplan.models import NumberPlan
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.db import transaction
from fsb.tariff.models import Tariff, TariffPlan

class TariffHandler(BaseHandler):
    """
    Authenticated entrypoint for blogposts.
     select t.digits, t.rate, t.tariff_plan_id from tariff t JOIN tariff_plan tp ON t.tariff_plan_id=tp.id  where digits IN (38067) ORDER BY digits DESC, rand();
    """
    allowed_methods = ('GET')
    model = Tariff
    #anonymous = 'AnonymousBlogpostHandler'
    fields = ('digits', 'name', 'country_code', 'rate', 'weeks', 'time_start', 'time_end')

    #@staticmethod
    #def resource_uri():
    #    return ('api_numberplan_handler', ['phone_number'])
    #@require_mime('json', 'yaml')
    def read(self, request, start=0, limit=50, tariff=None, phone=None):
        """
        Returns a blogpost, if `title` is given,
        otherwise all the posts.

        Parameters:
         - `phone_number`: The title of the post to retrieve.
        """
        #log.debug("read endpoint % s" % account)
        base = Tariff.objects
        if request.GET.get("start"):
            start = request.GET.get("start")
        if request.GET.get("limit"):
            limit = int(request.GET.get("limit"))
            limit += int(start)
        #return base.phone_tariff(phone, request.user)
        log.info(phone)
        try:
            if phone is not None:
                log.info(phone)
                resp = Tariff.objects.phone_tariff(phone, tariff)
                return {"rate": resp.rate }
            else:
                resp = base.filter(tariff_plan__id=tariff, enabled=True, tariff_plan__site__name__exact=request.user)[start:limit]
                count = base.filter(tariff_plan__id=tariff, enabled=True, tariff_plan__site__name__exact=request.user).count()
                return {"count": count, "tariff": resp}
        except:
            return rc.NOT_HERE

class TariffPlanHandler(BaseHandler):
    """
    Authenticated entrypoint for blogposts.
    """
    allowed_methods = ('GET')
    model = TariffPlan
    #anonymous = 'AnonymousBlogpostHandler'
    fields = ('id', 'name', 'cash_min', 'fee', 'fee_period', 'activation', 'enabled', 'date_start', 'date_end', 'primary', 'description')

    #@staticmethod
    #def resource_uri():
    #    return ('api_numberplan_handler', ['phone_number'])
    #@require_mime('json', 'yaml')
    def read(self, request, start=0, limit=50, tariff=None):
        """
        Returns a blogpost, if `title` is given,
        otherwise all the posts.

        Parameters:
         - `phone_number`: The title of the post to retrieve.
        """
        #log.debug("read endpoint % s" % account)
        base = TariffPlan.objects
        if request.GET.get("start"):
            start = request.GET.get("start")
        if request.GET.get("limit"):
            limit = int(request.GET.get("limit"))
            limit += int(start)
        #return base.all()
        try:
            if tariff is not None:
                return {"count": 1, "tariff_plan": base.get(pk=tariff, site__name__iexact=request.user)}
            else:
                resp = base.filter(site__name__iexact=request.user)[start:limit]
                count = base.filter(site__name__iexact=request.user).count()
                return {"count": count, "tariff_plan": resp}
        except:
            return rc.NOT_HERE