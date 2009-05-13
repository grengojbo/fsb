# -*- mode: python; coding: utf-8; -*-
"""
"""
from django.db import models
from django.db.models import Avg, Max, Min, Count
from fsbilling.tariff.models import TariffPlan as t
import csv, time, datetime
import logging
l = logging.getLogger('fsbilling.tariff.managers')

# Create your models here.
class TariffManager(models.Manager):
    def load_tariff(self, t, f):
        """
        Загрузка данных из csv файла
        для успешной загрузки тарифов необходимо в таблице TariffPlan прописать tariff_format 
        """
        save_cnt = 0
        #time_format = "%Y-%m-%d 00:00"
        time_format = "%d.%m.%Y 00:00"
        tf = t.tariff_format.split('|')
        try:
            reader = csv.reader(f, delimiter=tf[0])
            n = {}
            for row in reader:
                save_flag = False 
                for index, c in enumerate(gw.lcr_format.split(',')):
                    if c != 'other':
                        if c == 'digits' and len(row[index]) > 1:
                            save_flag = True
                        n[c]=row[index]
                # if save_flag:
                #     lc = self.model()
                #     lc.digits = n['digits']
                #     lc.name = n['name']
                #     # TODO проверка на неправильный формат, замена 5,12->5.12
                #     lc.rate = n['rate']
                #     lc.date_start = datetime.datetime.utcfromtimestamp(time.mktime(time.strptime(n['date_start'] + " 00:00", time_format)))
                #     l.debug(n['date_start'])
                #     try:
                #         lc.date_end = datetime.datetime.utcfromtimestamp(time.mktime(time.strptime(n['date_end'] + " 00:00", time_format)))
                #     except OverflowError, e:
                #        lc.date_end = datetime.datetime.max
                #     lc.lead_strip = 0
                #     lc.trail_strip = 0
                #     lc.quality = 0
                #     lc.reliability = 0
                #     lc.enabled = True
                #     lc.carrier_id = gw
                #     lc.save()
                #     save_cnt += 1
                    
                n.clear()
            return save_cnt
        except csv.Error, e:
            l.error('line %d: %s' % (reader.line_num, e))
            return save_cnt
                    
        #n = self.model()
        
        #n.uid = self.get_next_number()
        #n.password = User.objects.make_random_password(6, "0123456789")
        #n.accountcode = user
        # TODO: 
        #n.user_context = Context.objects.all()[0]
        #Context.objects.filter(default_context=True).values()[0]
        #n.effective_caller_id_name = user.username
        #n.enable = True
        #n.phone_type = 'S'
        #n.save()
        #l.debug(n.uid)
        #return n
        pass
    
