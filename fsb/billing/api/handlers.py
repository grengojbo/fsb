# -*- mode: python; coding: utf-8; -*-
from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.handler import PaginatedCollectionBaseHandler
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

class AccountHandler(PaginatedCollectionBaseHandler):
    """
    Working with User Accounts
    """
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = Balance
    fields = (('accountcode', ('username', 'email', 'first_name', 'last_name', 'date_joined', 'last_registered')), 'cash', ('tariff', ('id', 'name')),'enabled')

    #@staticmethod
    #def resource_uri():
    #    return ('api_numberplan_handler', ['phone_number'])

    #@require_mime('json', 'yaml')
    def read(self, request, account=None):
        """
        Returns a blogpost, if `title` is given,
        otherwise all the posts.

        Parameters:
         - `phone_number`: The title of the post to retrieve.
        """
        #s = Site.objects.get(name__iexact=request.user)
        self.resource_name = 'accounts'
        try:
            if account is not None:
                log.debug("read accounts %s" % account)
                return {"count": 1, "accounts": Balance.objects.get(accountcode__username__exact=account, site__name__exact=request.user)}
            else:
                #resp = base.filter(site__name__iexact=request.user)[start:limit]
                #count = base.filter(site__name__iexact=request.user).count()
                #return {"count": count, "accounts": resp}
                self.resources = Balance.objects.filter(site__name__exact=request.user)
                return super(AccountHandler, self).read(request)
        except:
            return rc.NOT_HERE

    @transaction.commit_on_success
    def update(self, request, account):
        """
        Update number plan type.
        """
        attrs = self.flatten_dict(request.POST)
        try:
            np = Balance.objects.get(accountcode__username__exact=account, site__name__exact=request.user)
            u = User.objects.get(balance=np)
            #np.nt=attrs['email']
            if attrs.get('first_name'):
                u.first_name = attrs.get('first_name')
            if attrs.get('last_name'):
                u.last_name = attrs.get('last_name')
            if attrs.get('password'):
                u.set_password(attrs.get('password'))
            if attrs.get("enabled") == "true":
                np.enabled = True
            elif attrs.get("enabled") == "true":
                np.enabled = False
            elif attrs.get("enable") == "true":
                np.enabled = True
            elif attrs.get("enable") == "true":
                np.enabled = False
            # TODO add disable User
            u.save()
            if attrs.get('tariff'):
                log.info('Change tarif: %i' % int(attrs.get('tariff')))
                np.tariff=TariffPlan.objects.get(pk=int(attrs.get('tariff')), enabled=True, site__name__exact=request.user)
            if attrs.get('email'):
                log.info('Change email: %s' % attrs.get('email'))
                u.email=attrs.get('email')
                u.save()
                np.accountcode = u
            np.save()
            return Balance.objects.get(accountcode__username__exact=account, site__name__exact=request.user)
        except:
            return rc.BAD_REQUEST

    @transaction.commit_on_success
    def delete(self, request, account):
        """
        Disable User Accounts
        """
        # TODO: tests and disable endpoint
        attrs = self.flatten_dict(request.POST)
        try:
            np = Balance.objects.get(accountcode__username__exact=account, site__name__exact=request.user)
            np.enabled = False
            np.save()
            return rc.DELETED
        except:
            return rc.NOT_HERE

    @transaction.commit_on_success
    def create(self, request):
        """
        Create new User Accounts
        """
        attrs = self.flatten_dict(request.POST)
        u = User.objects.get(username=request.user)
        s = Site.objects.get(name=request.user)
        active = False
        if attrs.get("enabled") == "true":
            active = True
        elif attrs.get("enabled") == "true":
            active = False
        elif attrs.get("enable") == "true":
            active = True
        elif attrs.get("enable") == "true":
            active = False
        if attrs.get('password'):
            password = attrs.get('password')
        else:
            password = User.objects.make_random_password()
        if attrs.get('tariff'):
            tariff = TariffPlan.objects.get(pk=int(attrs.get('tariff')), enabled=True, site__name__exact=request.user)
        else:
            tariff = TariffPlan.objects.get(primary=True, enabled=True, site__name__exact=request.user)
        try:
            #log.info(attrs.get('username'))
            #log.info(request.user)
            account =  User.objects.create(username=attrs.get("username"), email=attrs.get("email"), password=password)
            if attrs.get('first_name'):
                account.first_name = attrs.get('first_name')
            if attrs.get('last_name'):
                account.last_name = attrs.get('last_name')
            account.set_password(password)
            account.save()
            np = Balance.objects.get(accountcode=account)
            np.enabled = active
            np.tariff = tariff
            np.site = Site.objects.get(name=request.user)
            np.save()
            #resp = rc.ALL_OK
            #resp = rc.CREATED
            #resp.write(' - account created: %s' % attrs.get("username"))
            #return resp
            return Balance.objects.get(pk=np.pk)
        except:
            resp = rc.DUPLICATE_ENTRY
            #resp.write(' - username is not unique')
            return resp
