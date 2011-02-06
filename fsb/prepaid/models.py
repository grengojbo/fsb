# -*- mode: python; coding: utf-8; -*-
#
# Author:  Oleg Dolya --<oleg.dolya@gmail.com>
# Purpose:
# Created: 22.02.2010
#

__version__ = "$Revision$"
# $Source$

import datetime
from decimal import Decimal
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _
from l10n.utils import moneyfmt
from livesettings import config_value
from django.contrib.auth.models import User

import logging
from django.db.models import F, Q
from django.db.models import Max, Min, Avg, Sum, Count, StdDev, Variance
from fsb.billing.models import Balance, BalanceHistory
from fsa.directory.models import Endpoint


PREPAIDCODE_KEY = 'PREPAIDCODE'
log = logging.getLogger('prepaid.models')

N_TYPES = ((0, _(u'Partner')),
           (1, _(u'Default')),
           (2, _(u'Starting packet')),
           (3, _(u'Other')),
)
ST_TYPES = ((0, _(u'Нет такой карты')),
            (1, _(u'Карта невыдана')),
            (2, _(u'Неправильный ПИН код')),
            (3, _(u'Карта уже активирована')),
            (4, _(u'Ошибка ')),
            (5, _(u'Нормально')),
            (6, _(u'Неверный тип кары')),
)

class PrepaidManager(models.Manager):

##    def from_order(self, order):
##        code = order.get_variable(PREPAIDCODE_KEY, "")
##        log.debug("prepaidcert.from_order code=%s", code)
##        if code:
##            site = order.site
##            return Prepaid.objects.get(code__exact=code.value, valid__exact=True, site=site)
##        raise Prepaid.DoesNotExist()
    #----------------------------------------------------------------------
    def is_card(self, num, code):
        """
        Validate PIN code Prepaid Card

        Keyword arguments:
        num -- Number Card (SIP ID)
        code -- activate code

        Return:
        (Prepaid or None)
        """
        try:
            # TODO: сделать проверку по хешу
            card = self.get(num_prepaid__iexact=num, code__iexact=code, date_end__gte=datetime.date.today())
            return card
        except self.model.DoesNotExist:
            return False

    def create_starting(self):

        try:
            card = self.model()
#            new_user = User.objects.create_user(num, '', code)
#            new_endpoint = Endpoint.objects.create_endpoint(new_user)
#            comments = 'prepaid:::%i' % card.pk
#            if card.start_balance > 0:
#                BalanceHistory.objects.create(name='the starting packet is activated', accountcode=new_user,
#                                              cash=card.start_balance, comments=comments)
#                up_ball = Balance.objects.filter(accountcode=accountcode).update(cash=F('cash') + card.start_balance)
            card.enabled = True
            card.save(using=self._db)
#            # Ваш баланс был пополнен на
#            return (True, _("The starting packet is activated"), new_user)
            return card
        except:
            # Ваш баланс не пополнен
            #log.error(e)
#            return (False, _("Error code or number"), None)
            return false

    def add_prepaid(self, n):
        """
        Загрузка данных из csv файла
        """
        try:
            bl = self.model()
            bl.num_prepaid = n['num_prepaid'].strip()
            bl.code = n['code'].strip()
            bl.start_balance = n['rate']
            bl.nt = n['nt'].strip()
            bl.date_end = n['date_end']
            #bl.currency = currency
            bl.save()
            return 1
        except:
            log.error('add_prepaid')
            return 0

class Prepaid(models.Model):
    """A Prepaid Card which holds value."""
    num_prepaid = models.CharField(_(u'Number'), max_length=12, unique=True)
    code = models.CharField(_(u'Prepaid Code'), max_length=16, unique=True)
    date_added = models.DateField(_(u"Date added"), auto_now_add=True)
    date_end = models.DateField(_(u"Date end"), null=True, blank=True)
    nt = models.PositiveSmallIntegerField(_(u'Type'), max_length=1, choices=N_TYPES, default=1, blank=False)
    enabled = models.BooleanField(_(u'Enable'), default=False)
    valid = models.BooleanField(_(u'Issued'), default=False, help_text=_(u"only issued to the dealer's cards can be activated"))
    message = models.CharField(_(u'Message'), blank=True, null=True, max_length=254)
    start_balance = models.DecimalField(_(u"Starting Balance"), decimal_places=2, max_digits=8)
    diller = models.ForeignKey(User, verbose_name=_(u'Diller'), default=1)
    #currency = models.ForeignKey(CurrencyBase, default=1, related_name='currencys', verbose_name=_('Currency'))
    objects = PrepaidManager()

    def __unicode__(self):
        sb = moneyfmt(self.start_balance)
        return u"Prepaid Card: {0} {1}".format(self.num_prepaid, sb)

    @property
    def is_valid(self):
        if self.valid:
            return False
        return True

    class Meta:
        db_table = 'prepaid_prepaid'
        unique_together = ("num_prepaid", "code")
        verbose_name = _(u"Prepaid card")
        verbose_name_plural = _(u"Prepaid cards")

    def activate_card(self, accountcode):
        """Activate Prepaid Card"""
        try:
            #comments = 'prepaid:::%i' % self.pk
            #up_ball = Balance.objects.filter(accountcode=accountcode).update(cash=F('cash') + self.start_balance)
            # Ваш баланс был пополнен на
            #name='Added prepaid card'
            #BalanceHistory.objects.create(name=name, accountcode=accountcode, cash=self.start_balance, comments=comments)
            self.enabled = True
            self.save()
            return True
        except Exception, e:
            # Ваш баланс не пополнен
            #log.error(e)
            return None


    @property
    def balance(self):
        return moneyfmt(self.start_balance)

class PrepaidLogManager(models.Manager):
    def create_history(self, ipconnect, num_prepaid, code=None, username='AnonymousUser', st=0, nt=3):
        history = self.model(num_prepaid=num_prepaid, code=code, ipconnect=ipconnect, username=username, st=st, nt=nt)
        history.save(using=self._db)
        return history

    def is_valid(self, username=None, ipconnect=None):
        """
        Проверяем может ли пользователь с данного ip активировать кару
        """
        # TODO: добавить проверку по ip и username
        return True

class PrepaidLog(models.Model):
    num_prepaid = models.CharField(_(u'Number'), max_length=12, blank=True, null=True)
    code = models.CharField(_(u'Prepaid Code'), max_length=16, blank=True, null=True)
    nt = models.PositiveSmallIntegerField(_(u'Type'), max_length=1, choices=N_TYPES, blank=True, null=True)
    username = models.CharField(_(u'username'), max_length=30, blank=True, null=True)
    ipconnect = models.CharField(_(u'IP address'), max_length=39, blank=True, null=True)
    st = models.PositiveSmallIntegerField(_(u'Type'), max_length=1, choices=ST_TYPES, default=0)
    blocked = models.BooleanField(_(u'Blocked'), default=False)
    date_proces = models.DateTimeField(_(u'Date'), auto_now_add=True)
    objects = PrepaidLogManager()

    class Meta:
        db_table = 'prepaid_log'
        verbose_name = _(u"Log Activate")
        verbose_name_plural = _(u"Logs Activate")

    def __unicode__(self):
        return self.num_prepaid

#import config
#import listeners
#listeners.start_listening()
