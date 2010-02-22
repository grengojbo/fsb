# -*- mode: python; coding: utf-8; -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
#from payment.forms import SimplePayShipForm
from models import Prepaid

class PrepaidCodeForm(forms.Form):
    number = forms.CharField(_('Number'), required=True)
    code = forms.CharField(_('Code'), required=True)
    
    def clean(self):
        """
        Verify 
        """
        res, mes = Prepaid.objects.is_valid(self.cleaned_data.get("number"), self.cleaned_data.get("code"))
        if res:
            return self.cleaned_data
        else:
            raise forms.ValidationError(mes)
    
##class PrepaidPayShipForm(SimplePayShipForm):
##    prepaidnumber = forms.CharField(max_length=14)
##    prepaidcode = forms.CharField(max_length=14)
##    
##
##    def __init__(self, request, paymentmodule, *args, **kwargs):
##        super(PrepaidPayShipForm, self).__init__(request, paymentmodule, *args, **kwargs)
