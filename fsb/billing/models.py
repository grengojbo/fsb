# -*- mode: python; coding: utf-8; -*-
from django.db import models
#from lib.composition import ForeignCountField, CompositionField
#from django.db.models import signals
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from fsa.core.managers import GenericManager
from fsb.billing.managers import BalanceManager
from fsa.server.models import Server
#from fsb.tariff.models import TariffPlan
from django.db.models import Max, Min, Avg, Sum, Count, StdDev, Variance 
import datetime
from django.utils.dateformat import DateFormat
from django.utils.encoding import force_unicode
import os.path, csv, logging
from pytils.dt import ru_strftime
#from satchmo_utils.fields import CurrencyField
#from satchmo_store.contact.models import Contact
from decimal import Decimal

l = logging.getLogger('fsb.billing.models')

__author__ = '$Author$'
__revision__ = '$Revision$'

# Create your models here.
class Balance(models.Model):
    """(Balance description)"""
    accountcode = models.ForeignKey(User)
    #accountcode = models.ForeignKey(Contact)
    cash = models.DecimalField(_("Balance"), max_digits=18, decimal_places=10)
    #cash = CurrencyField(_("Balance"), max_digits=18, decimal_places=10, display_decimal=2)
    #tariff = models.ForeignKey(TariffPlan, related_name='tariffplangroup')
    enabled = models.BooleanField(_(u'Enable'), default=True)
    objects = BalanceManager() # default manager must be always on first place! It's used as default_manager
    active_objects = GenericManager( enabled = True ) # only active entries
    inactive_objects = GenericManager( enabled = False ) # only inactive entries
    timelimit= models.FloatField(_(u'Limit'), blank=False, default=0, help_text=_(u'Time limit'))
    #credit = CurrencyField(_("Discount Amount"), decimal_places=2, display_decimal=2, max_digits=8, default=Decimal("0.0"), help_text=_(u'Total sum for which credit is extended for calls'))
    credit = models.FloatField(_(u'Credit'), blank=False, default=0, help_text=_(u'Total sum for which credit is extended for calls'))
    
    class Meta:
        #ordering = []
        db_table = 'balance'
        verbose_name, verbose_name_plural = _(u"Balance"), _(u"Balances")

    def __unicode__(self):
        return self.accountcode.username

    @models.permalink
    def get_absolute_url(self):
        return ('Balance', [self.id])
   
    def cash_currency(self):
        """docstring for rate_currency"""
        return "%(rate)0.2f %(currency)s" % {'rate': self.cash, 'currency': self.currency}
    cash_currency.short_description = _(u'Баланс')

    @property
    def currency(self):
        return u'у.е.'
        
##class NibbleBill(models.Model):
##    """(NibbleBill description)"""
##    name = models.CharField(_(u'Name'), max_length=200)
##    server = models.ForeignKey(Server)
##    enabled = models.BooleanField(_(u'Enable'), default=True)
##    objects = models.Manager() # default manager must be always on first place! It's used as default_manager
##    active_objects = GenericManager( enabled = True ) # only active entries
##    inactive_objects = GenericManager( enabled = False ) # only inactive entries 
##
##    class Meta:
##        #ordering = []
##        db_table = 'nibblebill'
##        verbose_name, verbose_name_plural = _(u"Billing"), _(u"Billings")
##
##    def __unicode__(self):
##        return self.name
##
##    @models.permalink
##    def get_absolute_url(self):
##        return ('NibbleBill', [self.id])
        
##class CurrencyBase(models.Model):
##    """(CurrencyBase description)"""
##    name = models.CharField(_(u'Name'), max_length=200)
##    name_small = models.CharField(_(u'small'), max_length=10)
##    code = models.CharField(_(u'code'), max_length=3)
##    objects = models.Manager()
##    
##    class Meta:
##        #ordering = []
##        db_table = 'currency_base'
##        verbose_name, verbose_name_plural = _(u"Currency Base"), _(u"Currency Bases")
##
##    def __unicode__(self):
##        return self.name
##
##    @models.permalink
##    def get_absolute_url(self):
##        return ('CurrencyBase', [self.id])
        
##class Currency(models.Model):
##    """docstring for Currency"""
##    currency_name = models.ForeignKey(CurrencyBase)
##    rate = models.FloatField(_("Курс"), default=1)
##    date_start = models.DateTimeField(_(u'Date Start'))
##    date_end = models.DateTimeField(_(u'Date End'))
##    enabled = models.BooleanField(_(u'Enable'), default=True)
##    primary = models.BooleanField(_(u"Primary"), default=False)
##    objects = models.Manager() # default manager must be always on first place! It's used as default_manager
##    active_objects = GenericManager( enabled = True ) # only active entries
##    inactive_objects = GenericManager( enabled = False ) # only inactive entries
##    
##    @property
##    def enabled_date(self):
##        """docstring for enable_date"""
##        
##        if ru_strftime(format=u"%Y", date=self.date_end) == "2099":
##            de = ""
##        else:
##            de = " по %s" % ru_strftime(format=u"%d.%m.%Y", date=self.date_end)
##        return u"c %s%s" % (ru_strftime(format=u"%d.%m.%Y", date=self.date_start), de)
##        
##    @property
##    def rate_currency(self):
##        """docstring for rate_currency"""
##        return "%(rate)0.2f %(currency)s" % {'rate': self.rate, 'currency': self.currency_name.name_small}
##    
##    @models.permalink
##    def get_absolute_url(self):
##        return ('Currency', [self.id])
##
##    def __unicode__(self):
##        return self.currency_name.name
##    
##    class Meta:
##        ordering = ['-primary']
##        db_table = 'currency'
##        verbose_name, verbose_name_plural = _(u"Currency"), _(u"Currencys")
    
import config