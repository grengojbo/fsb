# -*- coding: UTF-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from fsadmin.core.managers import GenericManager

__author__ = '$Author:$'
__revision__ = '$Revision:$'

# Create your models here.
class NibbleBill(models.Model):
    """(NibbleBill description)"""
    name = models.CharField(_(u'Name'), max_length=200)
    server = models.ForeignKey(u'Server')
    enabled = models.BooleanField(_(u'Enable'), default=True)
    #active_objects = GenericManager( enabled = True ) # only active entries
    #inactive_objects = GenericManager( enabled = False ) # only inactive entries 

    class Meta:
        #ordering = []
        db_table = 'nibblrbill'
        verbose_name, verbose_name_plural = _(u"Billing"), _(u"Billings")

    def __unicode__(self):
        return self.name

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('NibbleBill', [self.id])
    
class TarifPlan(models.Model):
    """(Tarif description)"""
    name = models.CharField(_(u'Name'), max_length=80)    
    description = models.CharField(_(u'Description'), blank=True, max_length=240)

    class Meta:
        #ordering = []
        db_table = 'Tarif'
        verbose_name, verbose_name_plural = _(u"Tarif Plan"), _(u"Tarif Plans")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('Tarif', [self.id])
        
class Service(models.Model):
    """(Service description)"""
    name = models.CharField(_(u'Name'), max_length=80)    
    description = models.CharField(_(u'Description'), blank=True, max_length=240)

    class Meta:
        #ordering = []
        db_table = 'service'
        verbose_name, verbose_name_plural = _(u"Service"), _(u"Services")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('Services', [self.id])

#class Balance(models.Model):
#    """(Balance description)"""
#    accauntcode = models.ForeignKey(User)
#    cash = models.FloatField(_(u"Cash"))
#    tarif_plan = models.ForeignKey(TarifPlan)
#    service = models.ManyToManyField(Service)
#
#    class Meta:
#        #ordering = []
#        verbose_name, verbose_name_plural = "Balance", "Balances"
#
#    def __unicode__(self):
#        return u"Balance"
#
#    @models.permalink
#    def get_absolute_url(self):
#        return ('Balance', [self.id])