# -*- mode: python; coding: utf-8; -*-
from django.contrib import databrowse, admin
from django.utils.translation import ugettext_lazy as _
from fsb.tariff.models import TariffPlan, Tariff
import logging
l = logging.getLogger('fsb.tariff.admin')

class TariffPlanAdmin(admin.ModelAdmin):
    #date_hierarchy = ''
    list_display = ('id', 'name', 'cash_currency', 'fee_view', 'enabled_date', 'primary', 'enabled',)
    list_filter = ('enabled',)
    #search_fields = []

    #fieldsets = ()
    
    save_as = True
    save_on_top = True
    #inlines = []

class TariffAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_start'
    list_display = ('digits', 'enabled', 'name', 'rate', 'tariff_plan', 'enabled_date',)
    list_filter = ('enabled', 'tariff_plan',)
    list_editable = ('rate',)
    search_fields = ['digist']
    actions = ['delete_selected', 'make_enable', 'make_disable']

    fieldsets = ()
    
    save_as = True
    save_on_top = True
    list_per_page = 50
    #inlines = []
    
    def make_enable(self, request, queryset):
        rows_updated = queryset.update(enabled=True)
        if rows_updated == 1:
            message_bit = _(u"1 story was")
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as enabled." % message_bit)
    
    def make_disable(self, request, queryset):
        rows_updated = queryset.update(enabled=False)
        if rows_updated == 1:
            message_bit = _(u"1 story was")
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as disabled." % message_bit)
    
    make_disable.short_description = _(u"Mark selected stories as disable")
    make_enable.short_description = _(u"Mark selected stories as enable")

admin.site.register(Tariff, TariffAdmin)
admin.site.register(TariffPlan, TariffPlanAdmin)