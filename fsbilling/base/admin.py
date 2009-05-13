# -*- mode: python; coding: utf-8; -*-

from django.contrib import databrowse, admin
from django.utils.translation import ugettext_lazy as _
from fsbilling.base.models import NibbleBill
import logging
l = logging.getLogger('fsbilling.base.admin')

class BillingBaseAdmin(admin.ModelAdmin):
    #date_hierarchy = ''
    list_display = ('name', 'server', 'enabled',)
    list_filter = ('enabled',)
    #search_fields = []

    #fieldsets = ()
    
    save_as = True
    save_on_top = True
    #inlines = []

admin.site.register(NibbleBill, BillingBaseAdmin)