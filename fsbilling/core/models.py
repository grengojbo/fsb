# -*- coding: UTF-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

__author__ = '$Author:$'
__revision__ = '$Revision:$'

# Create your models here.
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
        ordering = []
        db_table = 'service'
        verbose_name, verbose_name_plural = _(u"Service"), _(u"Services")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('Services', [self.id])

class Balance(models.Model):
    """(Balance description)"""
    accauntcode = models.ForeignKey(User)
    cash = models.FloatField(_(u"Cash"))
    tarif_plan = models.ForeignKey(TarifPlan)
    service = models.ManyToManyField(Service)

    class Meta:
        #ordering = []
        verbose_name, verbose_name_plural = "Balance", "Balances"

    def __unicode__(self):
        return u"Balance"

    @models.permalink
    def get_absolute_url(self):
        return ('Balance', [self.id])