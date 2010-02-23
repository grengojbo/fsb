# -*- mode: python; coding: utf-8; -*-
#
# Author:  Oleg Dolya --<oleg.dolya@gmail.com>
# Purpose: 
# Created: 22.02.2010
#

__version__ = "$Revision$"  
# $Source$

from datetime import datetime
from decimal import Decimal
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _
from l10n.utils import moneyfmt
from livesettings import config_value
#from fsb.prepaid.utils import generate_certificate_code
#from fsb.billing.models import CurrencyBase
#from payment.utils import get_processor_by_key
#from product.models import Product, ProductManager
#from satchmo_store.contact.models import Contact
#from satchmo_store.shop.models import OrderPayment, Order
import logging
#import csv, sys, os
#from fsa.core.utils import CsvData
from django.db.models import F, Q
from django.db.models import Max, Min, Avg, Sum, Count, StdDev, Variance
from fsb.billing.models import Balance, BalanceHistory
from fsa.directory.models import Endpoint



PREPAIDCODE_KEY = 'PREPAIDCODE'
log = logging.getLogger('prepaid.models')

N_TYPES = ((0, _(u'Partner')),
           (1,_(u'Default')),
           (2,_(u'Starting packet')),
           (3,_(u'Other')),
        )
class PrepaidManager(models.Manager):

##    def from_order(self, order):
##        code = order.get_variable(PREPAIDCODE_KEY, "")
##        log.debug("prepaidcert.from_order code=%s", code)
##        if code:
##            site = order.site
##            return Prepaid.objects.get(code__exact=code.value, valid__exact=True, site=site)
##        raise Prepaid.DoesNotExist()
    #----------------------------------------------------------------------
    def is_valid(self, num,code, accountcode):
        """
        Validate Prepaid Card  
        
        Keyword arguments:
        num -- Number Card (SIP ID)
        code -- activate code
        accountcode -- User
        
        Return:
        (True/False, Message)
        """
        try:
            card = self.get(num_prepaid = num, code = code, date_end__gte = datetime.now(), nt = 1, enabled = False)
            comments = 'prepaid:::%i' % card.pk
            up_ball = Balance.objects.filter(accountcode=accountcode).update(cash=F('cash') + card.start_balance)
            # Ваш баланс был пополнен на
            name='Added prepaid card'
            BalanceHistory.objects.create(name=name, accountcode=accountcode, cash=card.start_balance, comments=comments)
            card.enabled =True
            card.save()
            return (True, _("Your balance was replenished"))
##                # этой картой вы неможете пополнить баланс
##                return (False, _("You cannot supplement the balance with this card"))
##                # эта карта уже активирована
##                #return (False, _("This card is already activated"))
        except Exception, e:
            # Ваш баланс не пополнен
            log.error(e)
            return (False, _("Your balance is not replenished. Error code or number"))
            
    def is_starting(self, num, code):
        """
        Activate Prepaid Card and create User  
        
        Keyword arguments:  
        num -- Number Card (SIP ID)  
        code -- activate code  
        
        Return:  
        (True/False, Message, Create User)
        """
        try:
            card = self.get(num_prepaid = num, code = code, date_end__gte = datetime.now(), nt = 2, enabled = False)
            new_user = User.objects.create_user(num, '', code)
            new_endpoint = Endpoint.objects.create_endpoint(new_user)
            comments = 'prepaid:::%i' % card.pk
            if card.start_balance > 0:
                BalanceHistory.objects.create(name='the starting packet is activated', accountcode=new_user, cash=card.start_balance, comments=comments)
                up_ball = Balance.objects.filter(accountcode=accountcode).update(cash=F('cash') + card.start_balance)
            card.enabled = True
            card.save()
            # Ваш баланс был пополнен на 
            return (True, _("The starting packet is activated"), new_user)
        except Exception, e:
            # Ваш баланс не пополнен
            log.error(e)
            return (False, _("Error code or number"), None)
        
    def add_prepaid(self, n):
        """
        
        """
        try:
            bl = self.model()
            bl.num_prepaid = n['num_prepaid']
            bl.code = n['code']
            bl.start_balance = n['rate']
            bl.nt = n['nt']
            bl.date_end = n['date_end']
            #bl.currency = currency
            bl.save()
            return 1
        except Exception, e:
            return 0

    def load_prepaid(self, currency, site, base_file):
        """
        Загрузка данных из csv файла
        """
        save_cnt = 0
        try:
            cd = CsvData(config_value('PAYMENT_PREPAID', 'FORMAT'))
            reader = csv.reader(base_file, delimiter=';', dialect='excel')
            no_base = []
            for row in reader:
                save_flag = False
                n = {}
                row_save = []
                n['date_end'] = datetime.max
                n['date_added'] = datetime.now()
                for index, c in enumerate(cd.data_col):
                    try:
                        #log.debug("%s=%s" % (c,row[index].strip()))
                        if c != 'zeros' and len(row[index].strip()) > 0:
                            if c == 'num_prepaid':
                                n["num_prepaid"] = row[index].strip()
                            elif c == 'code':
                                n["code"] = row[index].strip()
                                save_flag = True
                            elif c == 'start_balance':
                                n['start_balance'] = Decimal(cd.set_num(row[index].strip()))
                            elif c == 'date_added' and len(row[index].strip()) > 1:
                                n['date_added'] = cd.set_time(row[index].strip())
                            elif c == 'date_end' and len(row[index].strip()) > 1:
                                n['date_end'] = cd.set_time(row[index].strip())
                            elif row[index].strip() != '':
                                n[c]=row[index].strip()
                    except:
                        pass
                if save_flag:
                    save_cnt += self.add_prepaid(currency, site, n)
                    log.debug('Card number: %s' % n["num_prepaid"])
                n.clear()
        except csv.Error, e:
            log.error('line %d: %s' % (reader.line_num, e))
        return save_cnt

class Prepaid(models.Model):
    """A Prepaid Card which holds value."""
    #site = models.ForeignKey(Site, null=True, blank=True, verbose_name=_('Site'))
    #order = models.ForeignKey(Order, null=True, blank=True, related_name="prepaids", verbose_name=_('Order'))
    num_prepaid = models.CharField(_(u'Number'), max_length=12, unique=True)
    code = models.CharField(_('Prepaid Code'), max_length=12, unique=True)
    #purchased_by =  models.ForeignKey(Contact, verbose_name=_('Purchased by'),
    #    blank=True, null=True, related_name='prepaids_purchased')
    date_added = models.DateField(_("Date added"), auto_now_add = True)
    date_end = models.DateField(_("Date end"), null=True, blank=True)
    nt = models.PositiveSmallIntegerField(_(u'Type'), max_length=1, choices=N_TYPES, default=1, blank=False)
    enabled = models.BooleanField(_(u'Enable'), default=False)
    valid = models.BooleanField(_('Valid'), default=False)
    message = models.CharField(_('Message'), blank=True, null=True, max_length=254)
    start_balance = models.DecimalField(_("Starting Balance"), decimal_places=2, max_digits=8)
    #currency = models.ForeignKey(CurrencyBase, default=1, related_name='currencys', verbose_name=_('Currency'))
    objects = PrepaidManager()

    def __unicode__(self):
        sb = moneyfmt(self.start_balance)
        return u"Prepaid Card: %s %s" % (self.num_prepaid, sb)

    class Meta:
        unique_together = ("num_prepaid", "code")
        verbose_name = _("Prepaid card")
        verbose_name_plural = _("Prepaid cards")


    @property
    def balance(self):
        return moneyfmt(self.start_balance)
##
##        return b
##
##    def apply_to_order(self, order):
##        """Apply up to the full amount of the balance of this cert to the order.
##
##        Returns new balance.
##        """
##        amount = min(order.balance, self.balance)
##        log.info('applying %s from giftcert #%i [%s] to order #%i [%s]', 
##            moneyfmt(amount), 
##            self.id, 
##            moneyfmt(self.balance), 
##            order.id, 
##            moneyfmt(order.balance))
##            
##        processor = get_processor_by_key('PAYMENT_PREPAID')
##        orderpayment = processor.record_payment(order=order, amount=amount)
##        self.orderpayment = orderpayment
##        return self.use(amount, orderpayment=orderpayment)
##
##    def use(self, amount, notes="", orderpayment=None):
##        """Use some amount of the gift cert, returning the current balance."""
##        u = PrepaidUsage(notes=notes, balance_used = amount,
##            orderpayment=orderpayment, prepaid=self)
##        u.save()
##        return self.balance
##
##    def save(self, force_insert=False, force_update=False):
##        if not self.pk:
##            self.date_added = datetime.now()
##        if not self.code:
##            self.code = generate_certificate_code()
##        if not self.site:
##            self.site = Site.objects.get_current()
##        super(Prepaid, self).save(force_insert=force_insert, force_update=force_update)


##class PrepaidUsage(models.Model):
##    """Any usage of a Gift Cert is logged with one of these objects."""
##    usage_date = models.DateField(_("Date of usage"), null=True, blank=True)
##    notes = models.TextField(_('Notes'), blank=True, null=True)
##    balance_used = models.DecimalField(_("Amount Used"), decimal_places=2,
##        max_digits=8, )
##    orderpayment = models.ForeignKey(OrderPayment, null=True, verbose_name=_('Order Payment'))
##    used_by = models.ForeignKey(Contact, verbose_name=_('Used by'),
##        blank=True, null=True, related_name='prepaids_used')
##    prepaid = models.ForeignKey(Prepaid, related_name='usages')
##
##    def __unicode__(self):
##        return u"PrepaidUsage: %s" % self.balance_used
##
##    def save(self, force_insert=False, force_update=False):
##        if not self.pk:
##            self.usage_date = datetime.now()
##        super(PrepaidUsage, self).save(force_insert=force_insert, force_update=force_update)
##
##
##class PrepaidProduct(Product):
##    """
##    The product model for a Gift Certificate
##    """
##    objects = ProductManager()
##    #product = models.OneToOneField(Product, verbose_name=_('Product'), primary_key=True)
##    is_shippable = False
##    discountable = False
##    
##    #unit_price
##
##    def __unicode__(self):
##        return u"PrepaidProduct: %s" % self.name
##        
##    def _get_subtype(self):
##        return 'PrepaidProduct'        
##
##    def order_success(self, order, order_item):
##        log.debug("Order success called, creating prepaid card on order: %s", order)
##        for detl in order_item.orderitemdetail_set.all():
##            if detl.name == "message":
##                message = detl.value
##
##        price=order_item.line_item_price
##        log.debug("Creating gc for %s", price)
##        gc = Prepaid(
##            order = order,
##            start_balance= price,
##            purchased_by = order.contact,
##            valid=False,
##            message=message
##            )
##        gc.save()
##
##    class Meta:
##        verbose_name = _("Prepaid card product")
##        verbose_name_plural = _("Prepaid card products")

#import config
#import listeners
#listeners.start_listening()