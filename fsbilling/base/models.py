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
class NibbleBill(models.Model):
    """(NibbleBill description)"""
    name = models.CharField(_(u'Name'), max_length=200)
    server = models.ForeignKey(Server)
    enabled = models.BooleanField(_(u'Enable'), default=True)
    objects = models.Manager() # default manager must be always on first place! It's used as default_manager
    active_objects = GenericManager( enabled = True ) # only active entries
    inactive_objects = GenericManager( enabled = False ) # only inactive entries 

    class Meta:
        #ordering = []
        db_table = 'nibblebill'
        verbose_name, verbose_name_plural = _(u"Billing"), _(u"Billings")

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('NibbleBill', [self.id])
    