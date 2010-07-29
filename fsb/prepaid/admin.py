# -*- mode: python; coding: utf-8; -*-
from fsb.prepaid.models import Prepaid
#, PrepaidUsage, PrepaidProduct
from django.contrib import admin
from django.utils.translation import get_language, ugettext_lazy as _


#class PrepaidUsage_Inline(admin.StackedInline):
#    model = PrepaidUsage
#    extra = 1

class PrepaidOptions(admin.ModelAdmin):
    list_display = ('num_prepaid', 'enabled', 'valid', 'balance', 'date_end', 'nt',)
    list_display_links = ('num_prepaid',)
    search_fields = ['num_prepaid']
    search_fields_verbose = ['Number Card']
    list_filter = ('enabled', 'nt', 'start_balance',)
    ordering = ['date_added']
    #inlines = [PrepaidUsage_Inline]

admin.site.register(Prepaid, PrepaidOptions)
#admin.site.register(PrepaidProduct)

