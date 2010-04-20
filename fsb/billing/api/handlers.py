# -*- mode: python; coding: utf-8; -*-
from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import rc, require_mime, require_extended
#from piston.doc import generate_doc
import logging
from django.contrib.auth.models import User

log = logging.getLogger('fsb.billing.api.handlers')
from fsb.billing.models import Balance

class AccountHandler(BaseHandler):
    """
    Authenticated entrypoint for blogposts.
    """
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = Balance
    #anonymous = 'AnonymousBlogpostHandler'
    fields = (('accountcode', ('username', 'email')), 'cash', 'enabled', 'credit')

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
        log.debug("read accounts %s" % account)
        if request.GET.get("start"):
            start = request.GET.get("start")
        if request.GET.get("limit"):
            limit = int(request.GET.get("limit"))
            limit += int(start)
        base = Balance.objects
        if account:
            return {"count": 1, "accounts": base.get(accountcode__username=account)}
        else:
            return {"count": 1000, "accounts": base.all()[start:limit]}

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

    def create(self, request):
        """
        Update number plan type.
        """
        attrs = self.flatten_dict(request.POST)
        log.info(attrs.get("enabled"))
        if attrs.get("enabled") == "True":
            active = True
        else:
            active = False
        account =  User.objects.create(username=attrs.get("username"), email=attrs.get("email"))
        #np = Balance.objects.get(accountcode=account)
        #np.enables=False
        #np.save()

        return True
