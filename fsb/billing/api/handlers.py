# -*- mode: python; coding: utf-8; -*-
from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc, require_mime, require_extended
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from threaded_multihost.threadlocals import get_current_user, set_current_user
#from piston.doc import generate_doc
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
    fields = (('accountcode', ('username', 'email', 'password')), 'cash', ('tariff', ('id', 'name')),'enabled', 'credit')

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
                return {"count": 1000, "accounts": resp}
        except:
            return rc.NOT_HERE

    def update(self, request, account):
        """
        Update number plan type.
        """
        attrs = self.flatten_dict(request.POST)

        if self.exists(**attrs):
            return rc.DUPLICATE_ENTRY
        else:
            np = Balance.objects.get(accountcode=account)
            np.nt=attrs['nt']
            np.save()

            return np

    def delete(self, request, account):
        """
        Update number plan type.
        """
        attrs = self.flatten_dict(request.POST)

        np = Balance.objects.get(accountcode=account)
        np.enables=False
        np.save()

        return np
    
    @transaction.commit_on_success
    def create(self, request):
        """
        Update number plan type.
        """
        attrs = self.flatten_dict(request.POST)
        u = User.objects.get(username__iexact=request.user)
        s = Site.objects.get(name__iexact=request.user)
        if attrs.get("enabled") == "true":
            active = True
        else:
            active = False
            
        if attrs.get('password'):
            password = attrs.get('password')
        else:
            password = User.objects.make_random_password()
        try:
            account =  User.objects.create(username=attrs.get("username"), email=attrs.get("email"), password=password)
        except:
            resp = rc.DUPLICATE_ENTRY
            resp.write(' - username is not unique')
            return resp
        log.info(s)
        np = Balance.objects.get(contact=account)
        np.enables=active
        np.site = s
        np.save()

        return np
