# -*- mode: python; coding: utf-8; -*-
from django.db import models
from lib.composition import ForeignCountField, CompositionField
from django.conf import settings
from django.db.models import signals
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from fsa.core.managers import GenericManager
from fsb.tariff.managers import TariffManager
from fsa.server.models import Server
from django.db.models import Max, Min, Avg, Sum, Count, StdDev, Variance
import datetime
from django.utils.dateformat import DateFormat
from django.utils.encoding import force_unicode
import os.path, csv, logging
from pytils.dt import ru_strftime
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from bursar.fields import CurrencyField
from currency.fields import *
from currency.money import Money
from currency.models import Currency
from decimal import Decimal
l = logging.getLogger('fsb.tariff.models')

__author__ = '$Author:$'
__revision__ = '$Revision:$'

FEE_TARIFF_CHOICES = ((0, _(u'нет')), (1, _(u'ежедневно')), (2, _(u'ежемесячно')), (3, _(u'ежеквартально')), (4, _(u'каждые полгода')), (5, _(u'ежегодно')),)
OPERATOR_TYPE_CHOICES = (('F', _(u'Fixed')), ('M', _(u'Mobile')), ('N', _(u'Uncown')), ('S', _(u'Satelite')),)

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
    cash_min = CurrencyField(_("Плата за соединение"), max_digits=18, decimal_places=2, default=Decimal("0.00"), display_decimal=2)
    fee = CurrencyField(_("Абонплата"), max_digits=18, decimal_places=2, default=Decimal("0.00"), display_decimal=2)
    fee_period = models.SmallIntegerField(_(u'Период'), choices=FEE_TARIFF_CHOICES, default=0, help_text=_(u'период за который снимается абонентская плата'))
    activation = CurrencyField(_("Активация"), max_digits=18, decimal_places=2, default=Decimal("0.00"), display_decimal=4, help_text=_(u'стоимость активации тарифного плана'))
    date_start = models.DateTimeField(_(u'Date Start'), default=datetime.datetime.now())
    date_end = models.DateTimeField(_(u'Date End'), default=datetime.datetime.max)
    pay_round = models.SmallIntegerField(_(u'Округление'), default=1, help_text=_(u'Округляем стоимость разговора если 1 то до копейки для цен не поумолчанию'))
    enabled = models.BooleanField(_(u'Enable'), default=True)
    primary = models.BooleanField(_(u'По умолчанию'), default=False)
    site = models.ForeignKey(Site, default=1, verbose_name=_('Site'))
    #tariff_format = models.CharField(_(u'Tariff Format'), default="delimiter=';'time_format='%d.%m.%Y 00:00'lcr|country_code|special_digits|name|rate", max_length=250, help_text=_(u'Формат CSV файла для загрузки  тарифного плана'))
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


    def fee_view(self):
        """docstring for fee_view"""
        if self.fee_period != 0:
            return "%(rate)0.2f %(currency)s/%(fp)s/" % {'rate': self.fee, 'currency': self.currency, 'fp': self.get_fee_period_display()}
        else:
            return self.get_fee_period_display()
    fee_view.short_description = _(u'Абонплата')


    def cash_currency(self):
        """docstring for rate_currency"""
        return "%(rate)0.2f %(currency)s" % {'rate': self.cash_min, 'currency': self.currency}
    cash_currency.short_description = _(u'Плата за соединение.')

    @property
    def currency(self):
        return u'у.е.'

    @property
    def enabled_date(self):
        """docstring for enable_date"""

        if ru_strftime(format=u"%Y", date=self.date_end) == "2099":
            de = ""
        else:
            de = u" по %s" % ru_strftime(format=u"%d.%m.%Y", date=self.date_end)
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
    country_code = models.IntegerField(_(u'Country Code'), default=0)
    name_lcr = models.CharField(_(u'Направление по базе LCR'), max_length=200, blank=True)
    rate = CurrencyField(_(u"Стоимость"), max_digits=18, decimal_places=2, default=Decimal("0.0"), display_decimal=4)
    #price = MoneyField(max_digits=18, decimal_places=2, default=Money(0, Currency.objects.get_default()))
    price =  models.DecimalField(_(u'Price'), default=Decimal("0"), max_digits=18, decimal_places=4)
    price_currency = models.CharField(_(u'Currency name'), max_length=3, default="USD")
    tariff_plan = models.ForeignKey('TariffPlan', related_name='tpg')
    #tariff = models.ForeignKey(TariffPlan)
    date_start = models.DateTimeField(_(u'Date Start'), default=datetime.datetime.now())
    date_end = models.DateTimeField(_(u'Date End'), default=datetime.datetime.max)
    enabled = models.BooleanField(_(u'Enable'), default=True)
    weeks = models.SmallIntegerField(_(u'Week'), default=0)
    #weeks = models.CharField(_(u'Week'), max_length=13, default='1,2,3,4,5,6,7')
    #week1 = models.BooleanField(_(u'Monday'), default=True)
    #week2 = models.BooleanField(_(u'Tuesday'), default=True)
    #week3 = models.BooleanField(_(u'Wednesday'), default=True)
    #week4 = models.BooleanField(_(u'Thursday'), default=True)
    #week5 = models.BooleanField(_(u'Friday'), default=True)
    #week6 = models.BooleanField(_(u'Saturday'), default=True)
    #week7 = models.BooleanField(_(u'Sunday'), default=True)
    time_start = models.TimeField(_(u'Time Start'), default=datetime.datetime.strptime("00:00", "%H:%M"))
    time_end = models.TimeField(_(u'Time End'), default=datetime.datetime.strptime("23:59", "%H:%M"))
    cash_min = CurrencyField(_(u"Плата за соединение"), max_digits=18, decimal_places=2, default=Decimal("0.0"), display_decimal=2)
    time_round = models.SmallIntegerField(_(u'Округление'), default=1, help_text=_(u'Округляем время если 1 то до секунды, 60 до минуты, 30 то полминуты'))
    operator_type = models.CharField(_(u'Тип'), choices=OPERATOR_TYPE_CHOICES, max_length=1, default='N')
    #SmallIntegerField(_(u'Тип'), choices=, default=0, help_text=_(u'период за который снимается абонентская плата'))
    objects =TariffManager()
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
            de = u" по {0}".format(ru_strftime(format=u"%d.%m.%Y", date=self.date_end))
        return u"c {0}{1}".format(ru_strftime(format=u"%d.%m.%Y", date=self.date_start), de)


    def rate_currency(self):
        """docstring for rate_currency"""
        return "%(rate)0.2f %(currency)s" % {'rate': self.rate, 'currency': self.currency}
    rate_currency.short_description = _(u'Цена 1 мин.')

    @property
    def currency(self):
        return u'у.е.'


# Monkey-patching http://www.alrond.com/ru/2008/may/03/monkey-patching-in-django/
#from contact.models import Contact
#Contact.add_to_class('tariff',models.ForeignKey('fsb.tariff.TariffPlan',limit_choices_to = {'enabled': True}))
##Contact._meta.admin.fields += (('Additional', {'fields': ('tariff',)}),)
##Contact._meta.admin.list_display = Contact._meta.admin.list_display + ('tariff', )
##Contact._meta.admin.list_display += ('tariff', )

import listeners
listeners.start_listening()
