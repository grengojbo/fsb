# -*- mode: python; coding: utf-8; -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from fsb.billing.models import Balance, CreditBase, BalanceHistory
from fsa.directory.models import Endpoint
#from fsb.billing.models import NibbleBill
import logging

from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from grappelli.admin import GrappelliModelAdmin

UserAdmin.list_filter = ['is_staff', 'is_superuser', 'date_joined', 'last_login', 'groups', 'user_permissions']
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(Group, GroupAdmin)


#from grappelli.admin import GrappelliModelAdmin, GrappelliStackedInline, GrappelliTabularInline
log = logging.getLogger('fsb.billing.admin')

#admin.site.disable_action('delete_selected')

class BillingBaseAdmin(admin.ModelAdmin):
    #date_hierarchy = ''
    list_display = ('name', 'server', 'enabled',)
    list_filter = ('enabled',)
    #search_fields = []

    #fieldsets = ()

    save_as = True
    save_on_top = True
    #inlines = []
    list_per_page = 50

    def queryset(self, request):
        qs = super(BillingBaseAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(site=request.user)

##class CurrencyAdmin(admin.ModelAdmin):
##    list_display = ('rate_currency', 'enabled_date', 'primary', 'enabled',)
##    actions = ['delete_selected']
##
##    save_as = True
##    save_on_top = True
##    list_per_page = 50

class EndpointItemInline(admin.StackedInline):
    model = Endpoint
    classes = ('collapse open',)

class UserAdmin(admin.ModelAdmin):
    inlines= [EndpointItemInline]
    #list_display   = ('username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'is_staff', 'is_superuser')
    list_display   = ('username', 'date_joined', 'last_login', 'is_staff', 'is_superuser')
    search_fields  = ['username', 'first_name',  'last_name', 'email']
    date_hierarchy = 'date_joined'

class BalanceAdmin(admin.ModelAdmin):
    #list_display   = ('username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'is_staff', 'is_superuser')
    list_display = ('accountcode', 'username', 'cash_currency',  'tariff', 'timelimit', 'credit', 'enabled', 'site', 'last_login', 'date_joined',)
    #list_display = ('accountcode', 'cash_currency', 'timelimit', 'credit', 'tariff',)
    #actions = ['delete_selected']
    actions = None
    #readonly_fields = ['accountcode_name', 'credit', 'cash', 'last_login', 'date_joined']
    #inlines= [EndpointItemInline]
#    fieldsets = (
#        #(None, {'fields': ('username', 'password')}),
#        (None, {'fields': (('accountcode_name', 'cash', 'credit'), 'enabled')}),
#        #(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
#        (None, {'fields': ('tariff', 'timelimit', 'site')}),
#        (_('Important dates'), {'classes': ('collapse closed',), 'fields': (('last_login', 'date_joined'),)}),
#        #(_('Groups'), {'fields': ('groups',)}),
#    )



    save_as = True
    save_on_top = True
    list_per_page = 50

    class Media:
        verbose_name = _(u'Аккаунт')
        verbose_name_plural = _(u'Аккаунты')

class CreditBaseAdmin(GrappelliModelAdmin):
    list_display = ('__unicode__', 'credit', 'enabled','user', 'expire_time')
    #list_display = ('accountcode', 'cash_currency', 'timelimit', 'credit', 'tariff',)
    list_filter = ('enabled',)
    search_fields = ['balance__username']
    #actions = ['delete_selected']
    #readonly_fields = ['user']
    change_readonly_fields = ('balance', 'credit', 'expire_time')
    #raw_id_fields = ('balance',)
    autocomplete = {
        'balance': {
            'search_fields': ('username',),
            #'id_format':  'id',           # optional
            #'input_format':  'label',           # optional
            #'list_format':   'item.label',  # optional
            #'url': 'http://ws.geonames.org/searchJSON', # optional
            #'json_root': 'geonames', # optional
        }
    }
    fieldsets = (
        (None,{'fields': ('balance', 'enabled', 'credit', 'expire_time')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('balance', 'credit', 'expire_time')}
        ),
    )
    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return super(CreditBaseAdmin, self).get_fieldsets(request, obj)
        return self.change_readonly_fields

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(CreditBaseAdmin, self).get_fieldsets(request, obj)

    actions = None
    save_as = True
    save_on_top = True
    list_per_page = 50

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if not change:
            obj.enabled = True
        obj.save()

class BalanceHistoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'accountcode', 'amount', 'time_stamp','pay_date')
    #list_display = ('accountcode', 'cash_currency', 'timelimit', 'credit', 'tariff',)
    #actions = ['delete_selected']
    actions = None

    save_as = False
    save_on_top = False
    list_per_page = 50

admin.site.register(Balance, BalanceAdmin)
#admin.site.register(User, BalanceAdmin)
admin.site.register(CreditBase, CreditBaseAdmin)
admin.site.register(BalanceHistory, BalanceHistoryAdmin)
#admin.site.register(NibbleBill, BillingBaseAdmin)
admin.site.register(User, UserAdmin)