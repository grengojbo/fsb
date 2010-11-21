# -*- mode: python; coding: utf-8; -*-
from django.contrib import databrowse, admin
from django.utils.translation import ugettext_lazy as _
from fsb.tariff.models import TariffPlan, Tariff
from decimal import Decimal
import logging
l = logging.getLogger('fsb.tariff.admin')

class TariffPlanAdmin(admin.ModelAdmin):
    #date_hierarchy = ''
    list_display = ('id', 'name', 'cash_currency', 'fee_view', 'enabled_date', 'primary', 'enabled', 'site')
    list_filter = ('enabled',)
    #search_fields = []

    #fieldsets = ()
    
    save_as = True
    save_on_top = True
    #inlines = []

class TariffAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_start'
    list_display = ('digits', 'enabled', 'name', 'rate', 'price_view', 'tariff_plan', 'cash_min_view', 'time_round_view', 'enabled_date',)
    list_filter = ('enabled', 'tariff_plan',)
    list_editable = ('rate',)
    search_fields = ['digist']
    actions = ['delete_selected', 'make_enable', 'make_disable']

    fieldsets = ()
    
    save_as = True
    save_on_top = True
    list_per_page = 50
    #inlines = []

    def price_view(self, obj):
        if obj.price_currency == 'UAH':
            return u'{0} грн.'.format(obj.price)
        elif obj.price_currency == 'USD':
            return u'${0}'.format(obj.price)
        else:
            return u'{0}'.format(obj.price, obj.price_currency)
    price_view.short_description = _(u'Price')

    def cash_min_view(self, obj):
        if obj.cash_min > Decimal('0'):
            return obj.cash_min
        else:
            return _(u'нет')
    cash_min_view.short_description = _(u'Плата за соед...')

    def time_round_view(self, obj):
        if obj.time_round == 60:
            return _(u'1 мин.')
        else:
            return _(u'{0} сек.'.format(obj.time_round))
    time_round_view.short_description = _(u'Округл...')
    
    def make_enable(self, request, queryset):
        rows_updated = queryset.update(enabled=True)
        if rows_updated == 1:
            message_bit = _(u"1 story was")
        else:
            message_bit = "{0} stories were".format(rows_updated)
        self.message_user(request, "{0} successfully marked as enabled.".format(message_bit))
    
    def make_disable(self, request, queryset):
        rows_updated = queryset.update(enabled=False)
        if rows_updated == 1:
            message_bit = _(u"1 story was")
        else:
            message_bit = message_bit = "{0} stories were".format(rows_updated)
        self.message_user(request, "{0} successfully marked as enabled.".format(message_bit))
    
    make_disable.short_description = _(u"Mark selected stories as disable")
    make_enable.short_description = _(u"Mark selected stories as enable")

admin.site.register(Tariff, TariffAdmin)
admin.site.register(TariffPlan, TariffPlanAdmin)