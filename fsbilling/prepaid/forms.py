from django import forms
from django.utils.translation import ugettext_lazy as _
from payment.forms import SimplePayShipForm

class PrepaidCodeForm(forms.Form):
    code = forms.CharField(_('Code'), required=True)
    
class PrepaidPayShipForm(SimplePayShipForm):
    prepaidcode = forms.CharField(max_length=100)

    def __init__(self, request, paymentmodule, *args, **kwargs):
        super(PrepaidPayShipForm, self).__init__(request, paymentmodule, *args, **kwargs)
