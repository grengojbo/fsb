# -*- mode: python; coding: utf-8; -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import Prepaid, PrepaidLog
from fsb.billing.models import Balance, BalanceHistory
from django.db.models import F, Q
#from django.db.models import Max, Min, Avg, Sum, Count, StdDev, Variance
from fsa.directory.signals import endpoint_create
from fsa.directory.models import Endpoint
from django.contrib.auth.models import Group
from django.db import transaction
from decimal import Decimal
import time, datetime
import hashlib
import logging
import random
from django.contrib.auth.models import User
from uni_form.helpers import FormHelper, Submit, Reset
from uni_form.helpers import Layout, Fieldset, Row, HTML

log = logging.getLogger("fsb.prepaid.forms")
attrs_dict = {'class': 'required'}

class PrepaidForm(forms.Form):
    prnumber = forms.RegexField(label=_(u'Number'), required=True, regex=r'^\d+$',  max_length=12,
                        error_messages={'invalid': _(u"This value must contain only letters, numbers and underscores.")})
    prcode = forms.RegexField(label=_(u'PIN Code'), required=True, regex=r'^\d+$',  max_length=16,
                        error_messages={'invalid': _(u"This value must contain only letters, numbers and underscores.")})

class PrepaidCodeForm(PrepaidForm):
    helper = FormHelper()
    submit = Submit('activate', _(u'Activate'))
    helper.add_input(submit)

    #log.debug(request)
    def __init__(self, request, *args, **kwargs):
        super(PrepaidCodeForm, self).__init__(*args, **kwargs)
        self.user = request.user
        self.ip = request.META['REMOTE_ADDR']

    @transaction.commit_on_success
    def save_prepaid(self, res):
        try:
            bal = Balance.objects.get(accountcode__username__exact=self.user)
            pay_date = datetime.datetime.now()
            name = 'add:::lincom3000:::prepaid:::{0}'.format(res.pk)
            comments = 'Added prepaid card'
            method = 'from site prepaid'

            code = "{0}{1}{2}".format(name, comments, method)
            mcode = hashlib.md5()
            mcode.update(code.upper())

            temp_txt = "".join([str(random.randint(0, 9)) for i in range(20)])
            pay_transaction_id = "{0}X{1}".format(int(time.time()), temp_txt)
            transaction.commit()
            up_ball = Balance.objects.filter(accountcode__username__exact=self.user).update(
                    cash=F('cash') + res.start_balance)
            res.enabled = True
            res.save()
            log.debug("Prepaid enabled {0}".format(res.enabled))
            b = BalanceHistory.objects.create(name=name, accountcode=bal, site=bal.site, pay_date=pay_date,
                                              method=method, amount=Decimal(res.start_balance),
                                              transaction_id=pay_transaction_id, details=comments,
                                              reason_code=mcode.hexdigest())
            b.success = True
            b.save()
            return b
        except:
            #transaction.rollback()
            history = PrepaidLog.objects.create_history(self.ip, self.data.get("prnumber"), code=self.data.get("prcode"), st=4, nt=1)
            return False
        #else:
        #    transaction.commit()

    def clean(self):
        """
        Verify 
        """
        fl_error = False
        nt = 3
        st = 4
        try:
            #log.debug("number: {0} (user:{1}) ip: {2}".format(self.data.get("prnumber"), self.user, self.ip))
            prc = Prepaid.objects.get(num_prepaid__iexact=self.data.get("prnumber"))
        except Prepaid.DoesNotExist:
            #log.error("prnumber: {0} (user:{1}) ip: {2}".format(self.data.get("prnumber"), self.user, self.ip))
            history = PrepaidLog.objects.create_history(self.ip, self.data.get("prnumber"), username=self.user)
            #log.error(history.st)
            raise forms.ValidationError(_(u"Incorrect number or the code of the card."))
        try:
            log.debug("number: {0} code:{3} (user:{1}) ip: {2}".format(self.data.get("prnumber"), self.user, self.ip, self.data.get("prcode")))
            card = Prepaid.objects.is_card(self.data.get("prnumber"), self.data.get("prcode"))
            #log.debug("card: {0}".format(card))
            if card:
                if card.enabled:
                    st = 3
                    nt = card.nt
                    fl_error = True
                elif card.is_valid:
                    st = 1
                    nt = card.nt
                    fl_error = True
                elif card.nt == 1:
                    log.debug("RUN save_prepaid")
                    new_endpoint = self.save_prepaid(card)
                    if new_endpoint:
                        nt = card.nt
                        st = 5
                    else:
                        raise forms.ValidationError(_(u"System error no activate prepaid card!"))
                else:
                    st = 6
                    nt = card.nt
                    fl_error = True
            else:
                st = 2
                fl_error = True
        except:
            #log.error("number: {0} (user:{1}) ip: {2}".format(self.data.get("prnumber"), self.user, self.ip))
            #raise forms.ValidationError(_("System error no activate prepaid card!"))
            raise forms.ValidationError(_(u"Incorrect number or the code of the card."))
        #log.debug("st={0}".format(st))
        history = PrepaidLog.objects.create_history(self.ip, self.data.get("prnumber"), code=self.data.get("prcode"),
                                                    st=st, nt=nt, username=self.user)
        if fl_error:
            raise forms.ValidationError(_(u"Incorrect number or the code of the card."))
        return self.cleaned_data


class PrepaidStartForm(PrepaidForm):
    helper = FormHelper()
    submit = Submit('activate', _(u'Activate'))
    helper.add_input(submit)

    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_(u"Username"),
                                error_messages={'invalid': _(u"This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(label=_(u"Email address"), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u"Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u"Password (again)"))
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={ 'required': _(u"You must agree to the terms to register") })
    first_name = forms.CharField(label=_(u"first name"), max_length=30, required=False, widget=forms.TextInput())
    last_name = forms.CharField(label=_(u"last name"), max_length=30, required=False, widget=forms.TextInput())

    detail_help = _(u'Note. An optional field to fill.')
    email_help = _(u'Note. Your email address will not show anyone else. If you do not fill in this field, and forget your password you can not recover it.')
    password_help = _(u'From 6 to 20 characters, only letters and numbers. Note. Your password will not be shown to anyone else.')
    layout = Layout(
                    Fieldset(u'',
                             'prnumber',
                             'prcode',
                             ),

                    Fieldset(u'', 'username',
                             Row('password1','password2'),
                             HTML(password_help),
                             ),

                    # second fieldset shows the contact info
                    Fieldset(_(u'Additional Information'),
                            HTML(detail_help),
                            'email',
                            HTML(email_help),
                            'first_name',
                            'last_name',
                             ),
                    Fieldset(u'', 'tos',)
                    )

    helper.add_layout(layout)

    def __init__(self, request, *args, **kwargs):
        super(PrepaidStartForm, self).__init__(*args, **kwargs)
        self.user = request.user
        self.ip = request.META['REMOTE_ADDR']
        self.user_exits = True

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        self.user_exits = False
        raise forms.ValidationError(_(u"A user with that username already exists."))

    @transaction.commit_on_success
    def save_prepaid(self, card):
        try:
            #log.debug('email({0})'.format(self.data.get('email')))
            new_user = User.objects.create_user(self.data.get('username'), '', self.data.get('password1'))
            new_user.is_active = True
            user_group = Group.objects.get(name="user")
            new_user.groups.add(user_group)
            new_user.save()
            new_endpoint = Endpoint.objects.create_endpoint(new_user, self.data.get('prnumber'))
            #

            bal = Balance.objects.get(accountcode__username__exact=self.data.get('username'))
            pay_date = datetime.datetime.now()
            name = 'add:::lincom3000:::prepaid:::{0}'.format(card.pk)
            comments = 'Added Start Paskage'
            method = 'from site prepaid'

            code = "{0}{1}{2}".format(name, comments, method)
            mcode = hashlib.md5()
            mcode.update(code.upper())

            temp_txt = "".join([str(random.randint(0, 9)) for i in range(20)])
            pay_transaction_id = "{0}X{1}".format(int(time.time()), temp_txt)
            up_ball = Balance.objects.filter(accountcode__username__exact=self.data.get('username')).update(cash=F('cash') + card.start_balance)
            #log.debug("Prepaid enabled {0}".format(card.enabled))
            b = BalanceHistory.objects.create(name=name, accountcode=bal, site=bal.site, pay_date=pay_date,
                                              method=method, amount=Decimal(card.start_balance),
                                              transaction_id=pay_transaction_id, details=comments,
                                              reason_code=mcode.hexdigest())
            b.success = True
            b.save()
            card.enabled = True
            card.save()
            return new_endpoint
        except:
            #log.error(e)
            #transaction.rollback()
            history = PrepaidLog.objects.create_history(self.ip, self.data.get("prnumber"), code=self.data.get("prcode"), st=4, nt=2)
            return False


    def clean(self):
        fl_error = False
        nt = 3
        st = 4
        log.debug("len username: {0} user_exits:{1} tos:{2}".format(self.data.get('username'), self.user_exits, self.data.get('tos')))

        if self.user_exits and self.data.get('username') is not None and len(self.data.get('username')) > 0 and self.data.get('tos') is not None:
            if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
                if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                    raise forms.ValidationError(_(u"The two password fields didn't match."))
                else:
                    try:
                        #log.debug("number: {0} (user:{1}) ip: {2}".format(self.data.get("prnumber"), self.user, self.ip))
                        prc = Prepaid.objects.get(num_prepaid__iexact=self.data.get("prnumber"))
                    except Prepaid.DoesNotExist:
                        #log.error("prnumber: {0} (user:{1}) ip: {2}".format(self.data.get("prnumber"), self.user, self.ip))
                        history = PrepaidLog.objects.create_history(self.ip, self.data.get("prnumber"))
                        #log.error(history.st)
                        raise forms.ValidationError(_(u"Incorrect number or the code of the card."))
                    try:
                        #log.debug("number: {0} code:{3} (user:{1}) ip: {2}".format(self.data.get("prnumber"), self.user, self.ip, self.data.get("prcode")))
                        card = Prepaid.objects.is_card(self.data.get("prnumber"), self.data.get("prcode"))
                        #log.debug("card: {0}".format(card))
                        if card:
                            if card.enabled:
                                st = 3
                                nt = card.nt
                                fl_error = True
                            elif card.is_valid:
                                st = 1
                                nt = card.nt
                                fl_error = True
                            elif card.nt == 2:

                                log.debug("RUN save_prepaid")
                                new_endpoint = self.save_prepaid(card)
                                if new_endpoint:
                                    nt = card.nt
                                    st = 5
                                else:
                                    raise forms.ValidationError(_(u"System error no activate prepaid card!"))
                            else:
                                st = 6
                                nt = card.nt
                                fl_error = True
                        else:
                            st = 2
                            fl_error = True
                    except:
                        #log.error("number: {0} (user:{1}) ip: {2}".format(self.data.get("prnumber"), self.user, self.ip))
                        #raise forms.ValidationError(_("System error no activate prepaid card!"))
                        raise forms.ValidationError(_(u"Incorrect number or the code of the card."))
                    history = PrepaidLog.objects.create_history(self.ip, self.data.get("prnumber"), code=self.data.get("prcode"), st=st, nt=nt)
                    if fl_error:
                        raise forms.ValidationError(_(u"Incorrect number or the code of the card."))
            return self.cleaned_data
