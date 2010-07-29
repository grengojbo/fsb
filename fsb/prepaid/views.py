# -*- mode: python; coding: utf-8; -*-
from django import http
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
#from forms import PrepaidCodeForm, PrepaidPayShipForm
from models import Prepaid, PREPAIDCODE_KEY
from forms import PrepaidCodeForm
from livesettings import config_get_group, config_value
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
#from satchmo_store.shop.models import Order
#from payment.utils import pay_ship_save, get_or_create_order
#from payment.views import confirm, payship
#from satchmo_utils.dynamic import lookup_url
import logging
#from product.models import Product
#from satchmo_store.contact.models import AddressBook, Contact, ContactRole
#from satchmo_store.shop.models import Order, OrderItem, OrderItemDetail, Cart, CartItem, NullCart, NullCartItem
#from satchmo_store.shop.signals import satchmo_cart_changed, satchmo_cart_add_complete, satchmo_cart_details_query
from decimal import Decimal

log = logging.getLogger("fsb.prepaid.views")

gc = config_get_group('PAYMENT_PREPAID')

@login_required
def prepaid_form(request, template_name='prepaid/activate.html',
             success_url='profile_overview', extra_context=None, **kwargs):
    if request.method == "POST":
        form = PrepaidCodeForm(request, data=request.POST, files=request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            log.debug('form valid %s' % data)
            return redirect(success_url)
    else:
        form = PrepaidCodeForm(request)
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    
    return render_to_response(template_name, { 'form': form }, context_instance=context)

