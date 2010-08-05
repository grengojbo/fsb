# -*- mode: python; coding: utf-8; -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
#from payment.forms import SimplePayShipForm
from models import Prepaid
from fsb.billing.models import Balance, BalanceHistory
from django.db.models import F, Q
from django.db.models import Max, Min, Avg, Sum, Count, StdDev, Variance
from django.db import transaction
from decimal import Decimal
import time, datetime
import md5
import logging
import random
log = logging.getLogger("fsb.prepaid.forms")

class PrepaidCodeForm(forms.Form):
    prnumber = forms.CharField(label=_('Number'), required=True)
    prcode = forms.CharField(label=_('Code'), required=True)
    
    #log.debug(request)
    def __init__(self, request, *args, **kwargs):
        super(PrepaidCodeForm, self).__init__(*args, **kwargs)
        self.user = request.user
    
    @transaction.commit_manually
    def clean(self):
        """
        Verify 
        """
        log.debug("number: %s (%s)" % (self.data.get("prnumber"), self.user))
        res = Prepaid.objects.is_valid(self.data.get("prnumber"), self.data.get("prcode"))
        if res is None:
            raise forms.ValidationError(_("Incorrect number or the code of the card."))
        elif res.nt != 1:
            raise forms.ValidationError(_("You cannot supplement calculation with this card"))
        else:
            transaction.commit()
            try:
                bal = Balance.objects.get(accountcode__username__exact=self.user)
                pay_date = datetime.datetime.now()
                name = 'add:::lincom3000:::prepaid:::{0}'.format(res.pk)
                comments ='Added prepaid card'
                method = 'from site prepaid'
                
                code = "{0}{1}{2}".format(name, comments, method)
                mcode = md5.new()
                mcode.update(code.upper())
        
                temp_txt = "".join([str(random.randint(0, 9)) for i in range(20)])
                pay_transaction_id = "{0}X{1}".format(int(time.time()), temp_txt)
                up_ball = Balance.objects.filter(accountcode__username__exact=self.user).update(cash=F('cash') + res.start_balance)
                res.enabled = True
                res.save()
                log.debug("Prepaid enabled {0}".format(res.enabled))
                b = BalanceHistory.objects.create(name = name, accountcode= bal, site = bal.site, pay_date=pay_date, method = method, amount = Decimal(res.start_balance), transaction_id = pay_transaction_id, details=comments, reason_code=mcode.hexdigest())
                b.success = True
                b.save()
            except:
                transaction.rollback()
                raise forms.ValidationError(_("System error no activate prepaid card!"))
            else:
                transaction.commit()
        return self.cleaned_data
    
