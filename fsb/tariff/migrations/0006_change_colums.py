# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'TariffPlan.date_start'
        db.alter_column('tariff_plan', 'date_start', self.gf('django.db.models.fields.DateField')())

        # Changing field 'TariffPlan.date_end'
        db.alter_column('tariff_plan', 'date_end', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Tariff.date_start'
        db.alter_column('tariff', 'date_start', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Tariff.date_end'
        db.alter_column('tariff', 'date_end', self.gf('django.db.models.fields.DateField')())


    def backwards(self, orm):
        
        # Changing field 'TariffPlan.date_start'
        db.alter_column('tariff_plan', 'date_start', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'TariffPlan.date_end'
        db.alter_column('tariff_plan', 'date_end', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Tariff.date_start'
        db.alter_column('tariff', 'date_start', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Tariff.date_end'
        db.alter_column('tariff', 'date_end', self.gf('django.db.models.fields.DateTimeField')())


    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'tariff.tariff': {
            'Meta': {'object_name': 'Tariff', 'db_table': "'tariff'"},
            'cash_min': ('bursar.fields.CurrencyField', [], {'default': "'0.0'", 'max_digits': '18', 'decimal_places': '2'}),
            'code': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'country_code': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_end': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(9999, 12, 31)'}),
            'date_start': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2011, 1, 21)'}),
            'digits': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name_lcr': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'operator_type': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '18', 'decimal_places': '6'}),
            'price_currency': ('django.db.models.fields.CharField', [], {'default': "'USD'", 'max_length': '3'}),
            'rate': ('bursar.fields.CurrencyField', [], {'default': "'0.0'", 'max_digits': '18', 'decimal_places': '6'}),
            'tariff_plan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tpg'", 'to': "orm['tariff.TariffPlan']"}),
            'time_end': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(1900, 1, 1, 23, 59)'}),
            'time_round': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'time_start': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(1900, 1, 1, 0, 0)'}),
            'weeks': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        'tariff.tariffplan': {
            'Meta': {'ordering': "['-primary']", 'object_name': 'TariffPlan', 'db_table': "'tariff_plan'"},
            'activation': ('bursar.fields.CurrencyField', [], {'default': "'0.00'", 'max_digits': '18', 'decimal_places': '2'}),
            'cash_min': ('bursar.fields.CurrencyField', [], {'default': "'0.00'", 'max_digits': '18', 'decimal_places': '2'}),
            'date_end': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(9999, 12, 31)'}),
            'date_start': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2011, 1, 21)'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '240', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fee': ('bursar.fields.CurrencyField', [], {'default': "'0.00'", 'max_digits': '18', 'decimal_places': '2'}),
            'fee_period': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'pay_round': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"})
        }
    }

    complete_apps = ['tariff']
