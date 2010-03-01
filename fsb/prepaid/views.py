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

log = logging.getLogger("prepaid.views")

gc = config_get_group('PAYMENT_PREPAID')

@login_required
def prepaid_form(request, template_name='prepaid/activate.html',
             success_url='profile_overview', extra_context=None, **kwargs):
    if request.method == "POST":
        form = PrepaidCodeForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            #data = form.cleaned_data
            redirect(success_url)
    else:
        form = PrepaidCodeForm()
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    
    return render_to_response(template_name, { 'form': form }, context_instance=context)

##
##            # Create a new order.
##            newOrder = get_or_create_order(request, working_cart, contact, data)            
##            newOrder.add_variable(PREPAIDCODE_KEY, data['prepaidcode'])
##            
##            request.session['orderID'] = newOrder.id
##
##            url = None
##            if not url:
##                url = lookup_url(payment_module, 'satchmo_checkout-step3')
##                
##            return (True, http.HttpResponseRedirect(url))
##        form = PrepaidPayShipForm(request, payment_module)
##
##
##    
##def pay_ship_info(request):
##    cartplaces = config_value('SHOP', 'CART_PRECISION')
##    roundfactor = config_value('SHOP', 'CART_ROUNDING')
##    formdata = request.POST.copy()
##    if not formdata.has_key('productname'):
##        formdata['productname'] = 'prcard25'
##    productslug = formdata['productname']
##    details = []
##    try:
##        product = Product.objects.get(slug=productslug)
##        log.debug('found product: %s', product)
##        p_types = product.get_subtypes()
##        zero = Decimal("0.00")
##        ix = 0
##        for field in ('email', 'message'):
##            data = {
##                'name' : field,
##                'value' : formdata.get("custom_%s" % field, ""),
##                'sort_order' : ix,
##                'price_change' : zero,
##            }
##            ix += 1
##            details.append(data)
##        log.debug("Product Card detail: %s", details)
##        data = {}
##        #product, details = product_from_post(productslug, formdata)
##    except Product.DoesNotExist:
##        log.warn("Could not find product: %s", productslug)
##        product = None
##    working_cart = Cart.objects.from_request(request, create=True)
##    satchmo_cart_details_query.send(
##            working_cart,
##            product=product,
##            quantity=Decimal('1.0'),
##            details=details,
##            request=request,
##            form=formdata
##            )
##    try:
##        added_item = working_cart.add_item(product, number_added=Decimal('1.0'), details=details)
##        request.session['cart'] = working_cart.id
##        satchmo_cart_add_complete.send(working_cart, cart=working_cart, cartitem=added_item, product=product, request=request, form=formdata)
##    except Exception, e:
##        log.error('no add  working_cart.add_item')
##    satchmo_cart_changed.send(working_cart, cart=working_cart, request=request)
##    return payship.base_pay_ship_info(request, 
##        gc, 
##        prepaidcert_pay_ship_process_form,
##        template="shop/checkout/prepaid/pay_ship.html")
##    
##def confirm_info(request, template="shop/checkout/prepaid/confirm.html"):
##    try:
##        order = Order.objects.get(id=request.session['orderID'])
##        prepaidcert = Prepaid.objects.from_order(order)
##    except (Order.DoesNotExist, Prepaid.DoesNotExist, KeyError):
##        prepaidcert = None
##           
##    controller = confirm.ConfirmController(request, gc)
##    controller.templates['CONFIRM'] = template
##    controller.extra_context={'prepaidcert' : prepaidcert}
##    controller.confirm()
##    return controller.response
##
##def check_balance(request):
##    if request.method == "GET":        
##        code = request.GET.get('code', '')
##        if code:
##            try:
##                gc = Prepaid.objects.get(code=code, 
##                    value=True, 
##                    site=Site.objects.get_current())
##                success = True
##                balance = gc.balance
##            except Prepaid.DoesNotExist:
##                success = False
##        else:
##            success = False
##        
##        ctx = RequestContext(request, {
##            'code' : code,
##            'success' : success,
##            'balance' : balance,
##            'prepaid' : gc
##        })
##    else:
##        form = PrepaidCodeForm()
##        ctx = RequestContext(request, {
##            'code' : '',
##            'form' : form
##        })
##    return render_to_response(ctx, 'prepaid/balance.html')
