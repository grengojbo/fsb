# -*- mode: python; coding: utf-8; -*-
from django.db import models
from lib.composition import ForeignCountField, CompositionField
from django.conf import settings
from django.db.models import signals
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from fsa.core.managers import GenericManager
from fsadmin.server.models import Server
from django.db.models import Max, Min, Avg, Sum, Count, StdDev, Variance
import datetime
from django.utils.dateformat import DateFormat
from django.utils.encoding import force_unicode
import os.path, csv, logging
from pytils.dt import ru_strftime

l = logging.getLogger('fsb.tariff.models')

__author__ = '$Author:$'
__revision__ = '$Revision:$'

FEE_TARIFF_CHOICES = ((0, _(u'нет')), (1, _(u'ежедневно')), (2, _(u'ежемесячно')), (3, _(u'ежеквартально')), (4, _(u'каждые полгода')), (5, _(u'ежегодно')),)

# Create your models here.
class TariffPlan(models.Model):
    """
    Тарифный план
    Для загрузки тарифного плана из cvs файла необходимо установить его формат
    Например 
    tariff_format = ;|digits,name,tariff_rate,tariff,date_start=%d.%m.%Y 00:00,date_end
    ; - разделитель
    далее через запятую перечисляются поля для заполнения ВНИМАНИЕ все поля обязательны
    rate стоимость 1 минуты 0.338700
    date_start - Дата начала  01.12.08
    date_end - Дата окончания 31.12.99
    
    если есть пустая колонка то вставте other
    если формат даты отличается то необходимо указать формат date_start=%d.%m.%Y 00:00
    """
    name = models.CharField(_(u'Name'), max_length=80)
    cash_min = models.FloatField(_(u'Плата за соединение'), blank=False, default=0)
    fee = models.FloatField(_(u'Абонплата'), blank=False, default=0)
    fee_period = models.SmallIntegerField(_(u'Период'), choices=FEE_TARIFF_CHOICES, default=0, help_text=_(u'период за который снимается абонентская плата'))
    date_start = models.DateTimeField(_(u'Date Start'))
    date_end = models.DateTimeField(_(u'Date End'))
    enabled = models.BooleanField(_(u'Enable'), default=True)
    primary = models.BooleanField(_(u'По умолчанию'), default=False)
    tariff_format = models.CharField(_(u'Tariff Format'), default="delimiter=';'time_format='%d.%m.%Y 00:00'phone_number|first_name|last_name|zeros|gender|other", max_length=250, help_text=_(u'Формат CSV файла для загрузки  тарифного плана'))
    description = models.CharField(_(u'Description'), blank=True, max_length=240)
    objects = models.Manager() # default manager must be always on first place! It's used as default_manager
    active_objects = GenericManager( enabled = True ) # only active entries
    inactive_objects = GenericManager( enabled = False ) # only inactive entries

    class Meta:
        ordering = ['-primary']
        db_table = 'tariff_plan'
        verbose_name, verbose_name_plural = _(u"Тарифный план"), _(u"Тарифные планы")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('Tarif', [self.id])
    
    @property
    def fee_view(self):
        """docstring for fee_view"""
        if self.fee_period != 0:
            return "%(rate)0.2f %(currency)s/%(fp)s/" % {'rate': self.fee, 'currency': self.currency, 'fp': self.get_fee_period_display()}
        else:
            return self.get_fee_period_display()
        
    @property
    def cash_currency(self):
        """docstring for rate_currency"""
        return "%(rate)0.2f %(currency)s" % {'rate': self.cash_min, 'currency': self.currency}

    @property
    def currency(self):
        return u'у.е.'
        
    @property
    def enabled_date(self):
        """docstring for enable_date"""
        
        if ru_strftime(format=u"%Y", date=self.date_end) == "2099":
            de = ""
        else:
            de = " по %s" % ru_strftime(format=u"%d.%m.%Y", date=self.date_end)
        return u"c %s%s" % (ru_strftime(format=u"%d.%m.%Y", date=self.date_start), de)
        
class Tariff(models.Model):
    """
    digits - префикс передномером 4367890
    name - напрвление Austria-mobile Hutchison 3G
    tariff_plan - номер к какому тарифному плану относится смотреть id TariffPlan 
    """
    digits = models.CharField(_(u'Digits'), max_length=45, blank=True, help_text=_(u'matching digits'))
    # TODO: напрвление
    name = models.CharField(_(u'Направление'), max_length=200, blank=True)
    name_lcr = models.CharField(_(u'Направление по базе LCR'), max_length=200, blank=True)
    rate = models.FloatField(verbose_name=_(u"Стоимость"), default=0)
    tariff_plan = models.ForeignKey('TariffPlan', related_name='tpg')
    #tariff = models.ForeignKey(TariffPlan)
    date_start = models.DateTimeField(_(u'Date Start'))
    date_end = models.DateTimeField(_(u'Date End'))
    enabled = models.BooleanField(_(u'Enable'), default=True)
    objects = models.Manager() # default manager must be always on first place! It's used as default_manager
    active_objects = GenericManager( enabled = True ) # only active entries
    inactive_objects = GenericManager( enabled = False ) # only inactive entries

    class Meta:
        #ordering = []
        db_table = 'tariff'
        verbose_name, verbose_name_plural = _(u"Тариф"), _(u"Тарифы")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('Tariff', [self.id])
    
    @property
    def enabled_date(self):
        """docstring for enable_date"""
        
        if ru_strftime(format=u"%Y", date=self.date_end) == "2099":
            de = ""
        else:
            de = " по %s" % ru_strftime(format=u"%d.%m.%Y", date=self.date_end)
        return u"c %s%s" % (ru_strftime(format=u"%d.%m.%Y", date=self.date_start), de)
             
    @property
    def rate_currency(self):
        """docstring for rate_currency"""
        return "%(rate)0.2f %(currency)s" % {'rate': self.rate, 'currency': self.currency}
    
    @property
    def currency(self):
        return u'у.е.'
    
    
# Monkey-patching http://www.alrond.com/ru/2008/may/03/monkey-patching-in-django/
#from contact.models import Contact
#Contact.add_to_class('tariff',models.ForeignKey('fsb.tariff.TariffPlan',limit_choices_to = {'enabled': True}))
##Contact._meta.admin.fields += (('Additional', {'fields': ('tariff',)}),)                                             
##Contact._meta.admin.list_display = Contact._meta.admin.list_display + ('tariff', )                                    
##Contact._meta.admin.list_display += ('tariff', )