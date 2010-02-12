# -*- mode: python; coding: utf-8; -*-

from django.contrib import databrowse, admin
from django.utils.translation import ugettext_lazy as _
from fsb.profile.models import ProfileUser
import logging
l = logging.getLogger('fsb.profile.admin')

class ProfileUserAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    
admin.site.register(ProfileUser, ProfileUserAdmin)