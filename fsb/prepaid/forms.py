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
    #def __init__(self, request, data=None, files=None, user=None, *args, **kwargs):
    #    self.req = request
    #    super(PrepaidCodeForm, self).__init__(data=data, files=files, *args, **kwargs)
    #    self.user = user
    #def __init__(self, user, *args, **kwargs):
    #    super(ContactForm, self).__init__(*args, **kwargs)
    #    if not user.is_authenticated():
    #        self.fields['captcha'] = CaptchaField()
        
    def clean(self):
        """
        Verify 
        """
        res = Prepaid.objects.is_valid(self.data.get("prnumber"), self.data.get("prcode"))
        log.debug("number: %s" % self.data.get("prnumber"))
        if res is None:
            raise forms.ValidationError(_("Incorrect number or the code of the card."))
        elif res.nt != 1:
            raise forms.ValidationError(_("You cannot supplement calculation with this card"))
        return self.cleaned_data
    
