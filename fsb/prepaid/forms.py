# -*- mode: python; coding: utf-8; -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
#from payment.forms import SimplePayShipForm
from models import Prepaid
import logging
log = logging.getLogger("prepaid.forms")

class PrepaidCodeForm(forms.Form):
    number = forms.CharField(_('Number'), required=True)
    code = forms.CharField(_('Code'), required=True)
    
    #log.debug(request)
    #def __init__(self, request, data, *args, **kwargs):
    #    super(PrepaidCodeForm, self).__init__(request, number, data, *args, **kwargs)
        
    def clean(self):
        """
        Verify 
        """
        res, mes, user = Prepaid.objects.is_starting(self.data.get("number"), self.data.get("code"))
        if res:
            return self.data
        else:
            raise forms.ValidationError(mes)
    
