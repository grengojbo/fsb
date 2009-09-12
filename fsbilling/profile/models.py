# -*- mode: python; coding: utf-8; -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from userprofile.models import BaseProfile

__author__ = '$Author:$'
__revision__ = '$Revision:$'

# Create your models here.
class ProfileUser(BaseProfile):
    """(Profile description)"""
    regip = models.IPAddressField(_(u'IP Adress'), blank=True, null=True)
    objects = models.Manager()
    
    class Meta:
        #ordering = []
        db_table = 'profile_user'
        verbose_name, verbose_name_plural = _(u"Profile"), _(u"Profiles")

    def __unicode__(self):
        return self.user.username

    @models.permalink
    def get_absolute_url(self):
        return ('Profile', [self.id])

    