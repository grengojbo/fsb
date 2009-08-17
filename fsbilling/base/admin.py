# -*- mode: python; coding: utf-8; -*-

from django.contrib import databrowse, admin
from django.utils.translation import ugettext_lazy as _
from fsbilling.base.models import NibbleBill, CurrencyBase, Currency, Balance
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

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('rate_currency', 'enabled_date', 'primary', 'enabled',)
    actions = ['delete_selected']

    save_as = True
    save_on_top = True
    list_per_page = 50
    
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('accountcode', 'cash_currency', 'timelimit', 'credit', 'tariff',)
    actions = ['delete_selected']

    save_as = True
    save_on_top = True
    list_per_page = 50
class CurrencyBaseAdmin(admin.ModelAdmin):
    list_display = ('name_full', 'name', 'code',)
    actions = ['delete_selected']
    save_as = True
    save_on_top = True
    list_per_page = 50

admin.site.register(CurrencyBase, CurrencyBaseAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(NibbleBill, BillingBaseAdmin)