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
    #def __init__(self, data=None, files=None, user=None, *args, **kwargs):
    #    super(PrepaidCodeForm, self).__init__(*args, **kwargs)
    #    self.user = user
    #def __init__(self, user, *args, **kwargs):
    #    super(ContactForm, self).__init__(*args, **kwargs)
    #    if not user.is_authenticated():
    #        self.fields['captcha'] = CaptchaField()
        
    def clean(self):
        """
        Verify 
        """
        res, mes, user = Prepaid.objects.is_starting(self.data.get("number"), self.data.get("code"))
        #if res:
        #    return self.data
        #else:
        #    raise forms.ValidationError(mes)
        #raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data
    
