# -*- mode: python; coding: utf-8; -*-
from fsb.prepaid.models import Prepaid, PrepaidLog
#, PrepaidUsage, PrepaidProduct
from django.contrib import admin
from django.utils.translation import get_language, ugettext_lazy as _


#class PrepaidUsage_Inline(admin.StackedInline):
#    model = PrepaidUsage
#    extra = 1

class PrepaidAdmin(admin.ModelAdmin):
    list_display = ('num_prepaid', 'enabled', 'valid', 'balance', 'date_end', 'nt', 'diller', 'date_added',)
    list_display_links = ('num_prepaid',)
    search_fields = ['num_prepaid']
    search_fields_verbose = ['Number Card']
    list_filter = ('enabled', 'nt', 'start_balance',)
    ordering = ['date_added']
    list_per_page = 50

    fieldsets = (
        (None, {'fields': ('num_prepaid', 'diller', 'nt', 'enabled', 'valid', 'start_balance', 'date_end',)}),
    )

    change_readonly_fields = ('num_prepaid', 'nt', 'enabled', 'valid', 'start_balance', 'date_end',)

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return super(PrepaidAdmin, self).get_fieldsets(request, obj)
        return self.change_readonly_fields

class PrepaidLogAdmin(admin.ModelAdmin):
    list_display = ('num_prepaid', 'nt', 'st', 'username', 'blocked', 'ipconnect', 'date_proces',)
    list_display_links = ('num_prepaid',)
    search_fields = ['num_prepaid', 'username', 'ipconnect']
    search_fields_verbose = ['Number Card']
    list_filter = ('st', 'nt', 'blocked',)
    ordering = ['date_proces']
    list_per_page = 50

admin.site.register(Prepaid, PrepaidAdmin)
admin.site.register(PrepaidLog, PrepaidLogAdmin)

