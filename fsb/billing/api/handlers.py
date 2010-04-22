# -*- mode: python; coding: utf-8; -*-
from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc, require_mime, require_extended
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from threaded_multihost.threadlocals import get_current_user, set_current_user
#from piston.doc import generate_doc
from fsb.tariff.models import TariffPlan
from django.db import transaction

import logging

log = logging.getLogger('fsb.billing.api.handlers')
from fsb.billing.models import Balance

class AccountHandler(BaseHandler):
    """
    Authenticated entrypoint for blogposts.
    """
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = Balance
    #anonymous = 'AnonymousBlogpostHandler'
    fields = (('accountcode', ('username', 'email', 'date_joined')), 'cash', ('tariff', ('id', 'name')),'enabled', 'credit')

    #@staticmethod
    #def resource_uri():
    #    return ('api_numberplan_handler', ['phone_number'])
    #@require_mime('json', 'yaml')
    def read(self, request, start=0, limit=5, account=None):
        """
        Returns a blogpost, if `title` is given,
        otherwise all the posts.

        Parameters:
         - `phone_number`: The title of the post to retrieve.
        """
        #s = Site.objects.get(name__iexact=request.user)
        log.debug("read accounts %s" % account)
        if request.GET.get("start"):
            start = request.GET.get("start")
        if request.GET.get("limit"):
            limit = int(request.GET.get("limit"))
            limit += int(start)
        base = Balance.objects
        try:
            if account:
                return {"count": 1, "accounts": base.get(accountcode__username__iexact=account, site__name__iexact=request.user)}
            else:
                resp = base.filter(site__name__iexact=request.user)[start:limit]
                count = base.filter(site__name__iexact=request.user).count()
                return {"count": count, "accounts": resp}
        except:
            return rc.NOT_HERE

    @transaction.commit_on_success
    def update(self, request, account):
        """
        Update number plan type.
        """
        attrs = self.flatten_dict(request.POST)
        try:
            np = Balance.objects.get(accountcode__username__iexact=account, site__name__iexact=request.user)
            #np.nt=attrs['email']
            if attrs.get('tariff'):
                log.info('Change tarif: %i' % int(attrs['tariff']))
                np.tariff=TariffPlan.objects.get(pk=int(attrs['tariff']), enabled=True, site__name__iexact=request.user)
            if attrs.get('email'):
                log.info('Change email: %s' % attrs['email'])
                u = User.objects.get(balance=np)
                u.email=attrs['email']
                u.save()
                np.accountcode = u
            np.save()
            return np
        except:
            return rc.BAD_REQUEST

    @transaction.commit_on_success
    def delete(self, request, account):
        """
        Update number plan type.
        """
        attrs = self.flatten_dict(request.POST)
        try:
            np = Balance.objects.get(accountcode__username__iexact=account, site__name__iexact=request.user)
            np.enabled = False
            np.save()
            return rc.DELETED
        except:
            return rc.NOT_HERE
    
    @transaction.commit_on_success
    def create(self, request):
        """
        Update number plan type.
        """
        attrs = self.flatten_dict(request.POST)
        u = User.objects.get(username=request.user)
        s = Site.objects.get(name=request.user)
        if attrs.get("enabled") == "true":
            active = True
        else:
            active = False
            
        if attrs.get('password'):
            password = attrs.get('password')
        else:
            password = User.objects.make_random_password()
        if attrs.get('tariff'):
            tariff = TariffPlan.objects.get(pk=int(attrs.get('tariff')), enabled=True, site__name__iexact=request.user)
        else:
            tariff = TariffPlan.objects.get(primary=True, enabled=True, site__name__iexact=request.user)
        try:
            #log.info(attrs.get('username'))
            #log.info(request.user)
            account =  User.objects.create(username=attrs.get("username"), email=attrs.get("email"), password=password)
            np = Balance.objects.get(accountcode=account)
            np.enabled = active
            np.tariff = tariff
            np.site = Site.objects.get(name=request.user)
            np.save()
            return rc.CREATED
        except:
            resp = rc.DUPLICATE_ENTRY
            resp.write(' - username is not unique')
            return resp
