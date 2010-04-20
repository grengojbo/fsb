# -*- mode: python; coding: utf-8; -*-
"""
"""
from django.db import models
from django.db import connection
import logging, re, string, csv
import time, datetime
from fsa.core.utils import CsvData
#from django.template import Context, loader
from django.contrib.auth.models import User

from l10n.utils import moneyfmt
from livesettings import ConfigurationSettings, config_value, config_choice_values
#from fsadmin.dialplan.models import Context
from django.conf import settings
#from fsadmin.directory import Endpoint
from django.utils.encoding import force_unicode
from django.db.models import F, Q
from django.db.models import Max, Min, Avg, Sum, Count, StdDev, Variance
from decimal import Decimal
import logging

log = logging.getLogger('fsb.billing.managers')

class BalanceManager(models.Manager):
    def create_balance(self, contact, cash=None):
        """
        Баланс для нового пользователя
        create_balance
        """
        #from fsb.tariff.models import TariffPlan, Tariff
        #from fsb.profile.models import ProfileUser
        #from satchmo_store.contact.models import AddressBook, PhoneNumber, Contact, ContactRole
        log.info(site)
        try:
            bl = self.get(accountcode=contact)
            return bl
        except Exception, e:
            bl = self.model()
            bl.accountcode = contact
            bl.enabled = enabled
            #p = ProfileUser.objects.get(user=contact.user)
            log.info(site)
            if cash is None:
                # TODO сделать антиспам
                #bl.cash = config_value('SHOP','BALANCE_CASH')
                bl.cash = Decimal("0.0")
            else:
                bl.cash = Decimal(cash)
            if site is not None:
                bl.site = site
            #bl.cash = config_value('SHOP','BALANCE_CASH')
            #bl.tariff = TariffPlan.objects.get(enabled=True, primary=True)
            bl.save()
            return bl
    
# Create your models here.
