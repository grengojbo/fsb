# -*- mode: python; coding: utf-8; -*-
from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc, require_mime, require_extended
from django.contrib.auth.models import User
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from threaded_multihost.threadlocals import get_current_user, set_current_user
#from piston.doc import generate_doc
from fsb.billing.models import BalanceHistory, Balance
from django.db import transaction
from django.db.models import F

import logging

log = logging.getLogger('fsb.payments.api.handlers')

class PaymentsHandler(BaseHandler):
    """
    Authenticated entrypoint for blogposts.
    """
    allowed_methods = ('GET', 'POST', 'DELETE')
    model = BalanceHistory
    #anonymous = 'AnonymousBlogpostHandler'
    fields = ('name', 'accountcode', 'amount', 'transaction_id', 'time_stamp', 'success', 'details')

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
                return {"count": 1, "payment": base.get(accountcode__username__iexact=account, site__name__iexact=request.user)}
            else:
                resp = base.filter(site__name__iexact=request.user)[start:limit]
                count = base.filter(site__name__iexact=request.user).count()
                return {"count": count, "payment": resp}
        except:
            return rc.NOT_HERE

    @transaction.commit_manually
    def delete(self, request, account):
        """
        Update number plan type.
        """
        attrs = self.flatten_dict(request.POST)
        try:
            bal = Balance.objects.from_api_get(account, request.user)
            paymentargs = {
                "accountcode": bal,
                "name": attrs.get('name'),
                "site": Site.objects.get(name=request.user),
                "method" : 'from api payments',
                "transaction_id" : attrs.get('transaction_id'),
                "details" : attrs.get('details'),
            } 
        except Balance.DoesNotExist:
            log.error("DoesNotExist accountcode %s" % account)
            resp = rc.rc.NOT_HERE
            resp.write(' - "DoesNotExist accountcode %s' % account)
            return resp
        except Site.DoesNotExist:
            log.error("DoesNotExist user")
            resp = rc.rc.NOT_HERE
            resp.write(' - DoesNotExist user')
            return resp
        try:
            b = BalanceHistory.objects.create_linked(paymentargs, request.user, account, attrs.get('amount'))
            transaction.commit()
            bal.cash_del(b.amount)
            bal.save()
            b.success = True
            b.save()
        except:
            transaction.rollback()
            resp = rc.DUPLICATE_ENTRY
            resp.write(' - transaction_id is not unique')
            return resp
        else:
            transaction.commit()
            return {"transaction_id": b.transaction_id, "reason_code": b.reason_code, "success": b.success}
        
        
        try:
            np = Balance.objects.get(accountcode__username__iexact=account, site__name__iexact=request.user)
            np.enabled = False
            np.save()
            return rc.DELETED
        except:
            return rc.NOT_HERE
    
    @transaction.commit_manually
    def create(self, request):
        """
        Update number plan type.
        """
        attrs = self.flatten_dict(request.POST)
        bal = Balance.objects.from_api_get(attrs.get('accountcode'), request.user)
        try:
            bal = Balance.objects.from_api_get(attrs.get('accountcode'), request.user)
            paymentargs = {
                "accountcode": bal,
                "name": attrs.get('name'),
                "site": Site.objects.get(name=request.user),
                "method" : 'from api payments',
                "transaction_id" : attrs.get('transaction_id'),
                "details" : attrs.get('details'),
            } 
        except Balance.DoesNotExist:
            log.error("DoesNotExist accountcode %s" % attrs.get('accountcode'))
            resp = rc.rc.NOT_HERE
            resp.write(' - "DoesNotExist accountcode %s' % attrs.get('accountcode'))
            return resp
        except Site.DoesNotExist:
            log.error("DoesNotExist user")
            resp = rc.rc.NOT_HERE
            resp.write(' - DoesNotExist user')
            return resp
        try:
            b = BalanceHistory.objects.create_linked(paymentargs, request.user, attrs.get('accountcode'), attrs.get('amount'))
            transaction.commit()
            bal.cash_add(b.amount)
            bal.save()
            b.success = True
            b.save()
        except:
            transaction.rollback()
            resp = rc.DUPLICATE_ENTRY
            resp.write(' - transaction_id is not unique')
            return resp
        else:
            transaction.commit()
            return {"transaction_id": b.transaction_id, "reason_code": b.reason_code, "success": b.success}
