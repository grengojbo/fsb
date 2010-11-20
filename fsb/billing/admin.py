# -*- mode: python; coding: utf-8; -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from fsb.billing.models import Balance, CreditBase, BalanceHistory
from fsa.directory.models import Endpoint
#from fsb.billing.models import NibbleBill
from decimal import Decimal
import logging
import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from django import template
from django.db import transaction
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.html import escape
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

csrf_protect_m = method_decorator(csrf_protect)



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
    extra = 1

class UserAdmin(admin.ModelAdmin):
    inlines= [EndpointItemInline]

    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    diler_fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_filter = ('is_staff', 'is_active')
    #ordering = ('username',)
    filter_horizontal = ('user_permissions',)

    #list_display   = ('username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'is_staff', 'is_superuser')
    list_display   = ('username', 'email', 'balance_cash', 'balance_tariff', 'balance_site', 'format_date_joined', 'format_last_login', 'is_staff', 'is_superuser')
    search_fields  = ['username', 'first_name',  'last_name', 'email']
    date_hierarchy = 'date_joined'

    def balance_cash(self, obj):
        if obj.balance.credit > Decimal('0'):
            cash = obj.balance.cash + obj.balance.credit
            return "<b>{0:0.2f}</b>/{1}".format(cash, obj.balance.credit)
        elif obj.balance.cash < Decimal('0'):
            return '<span style="color: Red;"><b>{0:0.2f}</b></span>'.format(obj.balance.cash)
        else:
            return "<b>{0:0.2f}</b>".format(obj.balance.cash)
    balance_cash.short_description = _(u'Баланс/Кредит')
    balance_cash.allow_tags = True

    def balance_tariff(self,obj):
        return obj.balance.tariff
    balance_tariff.short_description = _(u'Тариф')

    def balance_site(self, obj):
        return obj.balance.site
    balance_site.short_description = _(u'Site')

    def format_date_joined(self, obj):
        return obj.date_joined.strftime('%d.%m.%Y')
    format_date_joined.short_description = _('date joined')

    def format_last_login(self, obj):
        return obj.last_login.strftime('%d.%m.%Y %H:%M')
    format_last_login.short_description = _('last login')

    def _prepare(self,request):
        """
        Подготовка нужных нам данных
        """
        # TODO: неработает
        user = request.user
        user.is_diller = bool(user.groups.filter(pk=1)) or user.is_superuser
        user.is_manager = not request.user.is_editor
        log.debug('Prepare User')

    def __call__(self, request, url):
        self._prepare(request)
        if url is None:
            return self.changelist_view(request)
        if url.endswith('password'):
            return self.user_change_password(request, url.split('/')[0])
        return super(UserAdmin, self).__call__(request, url)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(UserAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults.update({
                'form': self.add_form,
                'fields': admin.util.flatten_fieldsets(self.add_fieldsets),
            })
        defaults.update(kwargs)
        return super(UserAdmin, self).get_form(request, obj, **defaults)

    def get_urls(self):
        from django.conf.urls.defaults import patterns
        return patterns('',
            (r'^(\d+)/password/$', self.admin_site.admin_view(self.user_change_password))
        ) + super(UserAdmin, self).get_urls()

    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404('Your user does not have the "Change user" permission. In order to add users, Django requires that your user account have both the "Add user" and "Change user" permissions set.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        defaults = {
            'auto_populated_fields': (),
            'username_help_text': self.model._meta.get_field('username').help_text,
        }
        extra_context.update(defaults)
        return super(UserAdmin, self).add_view(request, form_url, extra_context)

    def user_change_password(self, request, id):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.model, pk=id)
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                new_user = form.save()
                msg = _('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': form.base_fields.keys()})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        return render_to_response(self.change_user_password_template or 'admin/auth/user/change_password.html', {
            'title': _('Change password: %s') % escape(user.username),
            'adminForm': adminForm,
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
            'root_path': self.admin_site.root_path,
        }, context_instance=RequestContext(request))

    def queryset(self, request):
        """
        Формируем queryset  для list-view

        Фильтруем пользователей по сайтам, только если мы не
        супер юзер или редактор
        """
        qs = super(UserAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            log.debug('user: {0}'.format(request.user))
            return qs.filter(balance__site__name__exact = request.user)

class BalanceAdmin(admin.ModelAdmin):
    #list_display   = ('username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'is_staff', 'is_superuser')
    #list_display = ('accountcode', 'username', 'cash_currency',  'tariff', 'timelimit', 'credit', 'enabled', 'site', 'last_login', 'date_joined',)
    list_display = ('accountcode', 'cash_currency', 'timelimit', 'credit', 'tariff',)
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