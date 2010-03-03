# -*- mode: python; coding: utf-8; -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
#from payment.forms import SimplePayShipForm
from models import Prepaid
import logging
log = logging.getLogger("prepaid.forms")

class PrepaidCodeForm(forms.Form):
    prnumber = forms.CharField(label=_('Number'), required=True)
    prcode = forms.CharField(label=_('Code'), required=True)
    
    #log.debug(request)
    def __init__(self, request, *args, **kwargs):
        super(PrepaidCodeForm, self).__init__(*args, **kwargs)
        self.user = request.user
        
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
            res.activate_card(self.user)
        return self.cleaned_data
    
