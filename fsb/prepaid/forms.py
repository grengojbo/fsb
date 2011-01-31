# -*- mode: python; coding: utf-8; -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import Prepaid, PrepaidLog
from fsb.billing.models import Balance, BalanceHistory
from django.db.models import F, Q
#from django.db.models import Max, Min, Avg, Sum, Count, StdDev, Variance
from fsa.directory.signals import endpoint_create
from fsa.directory.models import Endpoint
from django.db import transaction
from decimal import Decimal
import time, datetime
import hashlib
import logging
import random
from django.contrib.auth.models import User
from uni_form.helpers import FormHelper, Submit, Reset

log = logging.getLogger("fsb.prepaid.forms")
attrs_dict = {'class': 'required'}

class PrepaidCodeForm(forms.Form):
    prnumber = forms.CharField(label=_('Number'), required=True)
    prcode = forms.CharField(label=_('Code'), required=True)

    #log.debug(request)
    def __init__(self, request, *args, **kwargs):
        super(PrepaidCodeForm, self).__init__(*args, **kwargs)
        self.user = request.user
        self.ip = request.META['REMOTE_ADDR']

    @transaction.commit_manually
    def clean(self):
        """
        Verify 
        """
        log.debug("number: {0} (user:{1}) ip: {2}".format(self.data.get("prnumber"), self.user, self.ip))
        res = Prepaid.objects.is_valid(self.data.get("prnumber"), self.data.get("prcode"))
        if res is None:
            raise forms.ValidationError(_("Incorrect number or the code of the card."))
        elif res.nt != 1:
            raise forms.ValidationError(_("You cannot supplement calculation with this card"))
        else:
            transaction.commit()
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
            except:
                transaction.rollback()
                raise forms.ValidationError(_("System error no activate prepaid card!"))
            else:
                transaction.commit()
        return self.cleaned_data

class PrepaidForm(forms.Form):
    prnumber = forms.RegexField(label=_('Number'), required=True, regex=r'^\d+$',  max_length=12,
                        error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    prcode = forms.RegexField(label=_('Code'), required=True, regex=r'^\d+$',  max_length=16,
                        error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})

    helper = FormHelper()
    submit = Submit('passreset', _('Reset my password'))
    helper.add_input(submit)

class PrepaidStartForm(PrepaidForm):

    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(label=_("Email address"), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password (again)"))

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
        raise forms.ValidationError(_("A user with that username already exists."))

    transaction.commit_manually
    def clean(self):
        fl_error = False
        nt = 3
        log.debug("len username: {0} user_exits:{1}".format(self.data.get('username'), self.user_exits))

        if self.user_exits and self.data.get('username') is not None and len(self.data.get('username')) > 0:
            if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
                if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                    raise forms.ValidationError(_(u"The two password fields didn't match."))
            try:
                #log.debug("number: {0} (user:{1}) ip: {2}".format(self.data.get("prnumber"), self.user, self.ip))
                prc = Prepaid.objects.get(num_prepaid__iexact=self.data.get("prnumber"))
            except Prepaid.DoesNotExist:
                log.error("prnumber: {0} (user:{1}) ip: {2}".format(self.data.get("prnumber"), self.user, self.ip))
                history = PrepaidLog.objects.create_history(self.ip, self.data.get("prnumber"))
                raise forms.ValidationError(_(u"Incorrect number or the code of the card."))
            try:
                card = Prepaid.objects.is_card(self.data.get("prnumber"), self.data.get("prcode"))
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
                        nt = card.nt
                        st = 5
                        transaction.commit()
                        try:
                            new_user = User.objects.create_user(self.data.get('username'), self.data.get('email'), self.data.get('password1'))
                            new_user.is_active = True
                            new_user.save()
                            new_endpoint = Endpoint.objects.create_endpoint(new_user, self.data.get('prnumber'))
                            endpoint_create.send(sender=self.__class__, endpoint=new_endpoint)

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
                            card.enabled = True
                            card.save()
                            log.debug("Prepaid enabled {0}".format(card.enabled))
                            b = BalanceHistory.objects.create(name=name, accountcode=bal, site=bal.site, pay_date=pay_date,
                                                  method=method, amount=Decimal(card.start_balance),
                                                  transaction_id=pay_transaction_id, details=comments,
                                                  reason_code=mcode.hexdigest())
                            b.success = True
                            b.save()
                        except:
                            transaction.rollback()
                            history = PrepaidLog.objects.create_history(self.ip, self.data.get("prnumber"), code=self.data.get("prcode"), st=4, nt=2)
                            raise forms.ValidationError(_("System error no activate prepaid card!"))
                        else:
                            transaction.commit()
                    else:
                        st = 6
                        nt = card.nt
                        fl_error = True
                else:
                    st = 2
                    fl_error = True
            except Exception, e:
                log.error(e)
                log.error("number: {0} (user:{1}) ip: {2}".format(self.data.get("prnumber"), self.user, self.ip))
                #raise forms.ValidationError(_("System error no activate prepaid card!"))
                raise forms.ValidationError(_(u"Incorrect number or the code of the card."))
            history = PrepaidLog.objects.create_history(self.ip, self.data.get("prnumber"), code=self.data.get("prcode"), st=st, nt=nt)
            if fl_error:
                raise forms.ValidationError(_(u"Incorrect number or the code of the card."))

        return self.cleaned_data
