# -*- mode: python; coding: utf-8; -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from fsadmin.core.managers import GenericManager
from fsadmin.server.models import Server

__author__ = '$Author:$'
__revision__ = '$Revision:$'



# Create your models here.
class TariffPlan(models.Model):
    """
    Тарифный план
    Для загрузки тарифного плана из cvs файла необходимо установить его формат
    Например 
    tariff_format = ;|digits,name,tariff_rate,tariff,date_start=%d.%m.%Y 00:00,date_end
    ; - разделитель
    далее через запятую перечисляются поля для заполнения ВНИМАНИЕ все поля обязательны
    digits - префикс передномером 4367890
    name - напрвление Austria-mobile Hutchison 3G
    tariff_rate стоимость 1 минуты 0.338700
    tariff - номер к какому тарифному плану относится смотреть id TariffPlan 
    date_start - Дата начала  01.12.08
    date_end - Дата окончания 31.12.99
    
    если есть пустая колонка то вставте other
    если формат даты отличается то необходимо указать формат date_start=%d.%m.%Y 00:00
    """
    name = models.CharField(_(u'Name'), max_length=80)    
    description = models.CharField(_(u'Description'), blank=True, max_length=240)
    enabled = models.BooleanField(_(u'Enable'), default=True)
    tariff_format = models.CharField(_(u'Tariff Format'), max_length=200, blank=True, default="digits,name,tariff_rate,tariff,date_start,date_end", help_text=_(u'Format file to load Tariff'))
    objects = models.Manager() # default manager must be always on first place! It's used as default_manager
    active_objects = GenericManager( enabled = True ) # only active entries
    inactive_objects = GenericManager( enabled = False ) # only inactive entries

    class Meta:
        #ordering = []
        db_table = 'tariff_plan'
        verbose_name, verbose_name_plural = _(u"Tariff Plan"), _(u"Tariff Plans")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('Tarif', [self.id])
        
class Tariff(models.Model):
    """(Tariff description)"""
    digits = models.CharField(_(u'Digits'), max_length=45, blank=True, help_text=_(u'matching digits'))
    # TODO: напрвление
    name = models.CharField(_(u'Country'), max_length=200, blank=True)
    tariff_rate = models.FloatField(_(u'Rate'))
    tariff = models.ForeignKey(TariffPlan)
    date_start = models.DateTimeField(_(u'Date Start'))
    date_end = models.DateTimeField(_(u'Date End'))
    enabled = models.BooleanField(_(u'Enable'), default=True)
    objects = models.Manager() # default manager must be always on first place! It's used as default_manager
    active_objects = GenericManager( enabled = True ) # only active entries
    inactive_objects = GenericManager( enabled = False ) # only inactive entries

    class Meta:
        #ordering = []
        db_table = 'Tariff'
        verbose_name, verbose_name_plural = _(u"Tariff"), _(u"Tariffs")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('Tariff', [self.id])
        

# Monkey-patching http://www.alrond.com/ru/2008/may/03/monkey-patching-in-django/
#from contact.models import Contact
#Contact.add_to_class('tariff',models.ForeignKey('fsbilling.tariff.TariffPlan',limit_choices_to = {'enabled': True}))
##Contact._meta.admin.fields += (('Additional', {'fields': ('tariff',)}),)                                             
##Contact._meta.admin.list_display = Contact._meta.admin.list_display + ('tariff', )                                    
##Contact._meta.admin.list_display += ('tariff', )