# -*- mode: python; coding: utf-8; -*-
"""
"""
from django.db import models
from django.db import connection
import logging, re, string, csv
import time, datetime
from fsadmin.core.utils import CsvData
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
import logging
l = logging.getLogger('fsbilling.base.managers')

class BalanceManager(models.Manager):
    def create_balance(self, contact):
        """
        Баланс для нового пользователя
        """
        from fsbilling.tariff.models import TariffPlan, Tariff
        bl = self.model()
        bl.accountcode = contact
        bl.cash = config_value('SHOP','BALANCE_CASH')
        bl.tariff = TariffPlan.objects.get(enabled=True, primary=True)
        bl.save()
        return bl
    
# Create your models here.
