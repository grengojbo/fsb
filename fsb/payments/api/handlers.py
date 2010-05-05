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
from decimal import Decimal
import md5

import logging

log = logging.getLogger('fsb.payments.api.handlers')

class PaymentsHandler(BaseHandler):
    """
    Authenticated entrypoint for blogposts.
    """
    allowed_methods = ('GET', 'POST')
    model = BalanceHistory
    #anonymous = 'AnonymousBlogpostHandler'
    #fields = ('name', 'accountcode', 'amount', 'transaction_id', 'time_stamp', 'success', 'details')
    fields = ('name', 'username', 'amount', 'transaction_id', 'time_stamp', 'details', 'success')

    #@staticmethod
    #def resource_uri():
    #    return ('api_numberplan_handler', ['phone_number'])
    #@require_mime('json', 'yaml')
    def read(self, request, start=0, limit=5, account=None, transaction_id=None):
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
        base = BalanceHistory.objects
        try:
            if transaction_id is not None:
                return {"count": 1, "payment": base.get(transaction_id=transaction_id, site__name__exact=request.user)}
            elif account is not None:
                bal = Balance.objects.from_api_get(account, request.user)
                resp = base.filter(accountcode=bal, site__name__exact=request.user)[start:limit]
                count = base.filter(accountcode=bal, site__name__exact=request.user).count()
                return {"count": count, "payment": resp}
            else:
                resp = base.filter(site__name__exact=request.user)[start:limit]
                count = base.filter(site__name__exact=request.user).count()
                return {"count": count, "payment": resp}
        except:
            return rc.NOT_HERE

    @transaction.commit_manually
    def create(self, request):
        """
        Update number plan type.
        """
        attrs = self.flatten_dict(request.POST)
        #b = BalanceHistory.objects.create_linked(paymentargs, request.user, attrs.get('accountcode'), attrs.get('amount'))
        try:
            bal = Balance.objects.from_api_get(attrs.get('username'), request.user)
        except Balance.DoesNotExist:
            log.error("DoesNotExist username %s" % attrs.get('username'))
            resp = rc.rc.NOT_HERE
            resp.write(' - "DoesNotExist username %s' % attrs.get('username'))
            return resp
        except Site.DoesNotExist:
            log.error("DoesNotExist user")
            resp = rc.rc.NOT_HERE
            resp.write(' - DoesNotExist user')
            return resp
        try:
            code = "".join(attrs.get('username')).join(attrs.get('amount')).join(attrs.get('transaction_id')).join(attrs.get('details')).join(attrs.get('name')).join(str(request.user))
            mcode = md5.new()
            mcode.update(code.upper())
            b = BalanceHistory.objects.create(name = attrs.get('name'), accountcode= bal, site = Site.objects.get(name=request.user),
                method = 'from api payments', amount = Decimal(attrs.get('amount')), transaction_id = attrs.get('transaction_id'),
                details=attrs.get('details'), reason_code=mcode.hexdigest())
            b.save()
            transaction.commit()
            if Decimal(b.amount) < Decimal('0'):
                bal.cash_del(b.amount)
                if bal.is_positiv:
                    bal.save()
                    b.success = True
                    b.save()
            else:
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
