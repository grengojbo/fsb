# -*- mode: python; coding: utf-8; -*-

from south.db import db
from django.db import models
from fsbilling.base.models import *
from satchmo_utils.fields import CurrencyField
from payment.fields import PaymentChoiceCharField, CreditChoiceCharField
from shipping.fields import ShippingChoiceCharField

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Balance'
        db.create_table('balance', (
            ('id', orm['base.Balance:id']),
            ('accountcode', orm['base.Balance:accountcode']),
            ('cash', orm['base.Balance:cash']),
            ('tariff', orm['base.Balance:tariff']),
            ('enabled', orm['base.Balance:enabled']),
            ('timelimit', orm['base.Balance:timelimit']),
            ('credit', orm['base.Balance:credit']),
        ))
        db.send_create_signal('base', ['Balance'])
        
        # Adding model 'Currency'
        db.create_table('currency', (
            ('id', orm['base.Currency:id']),
            ('currency_name', orm['base.Currency:currency_name']),
            ('rate', orm['base.Currency:rate']),
            ('date_start', orm['base.Currency:date_start']),
            ('date_end', orm['base.Currency:date_end']),
            ('enabled', orm['base.Currency:enabled']),
            ('primary', orm['base.Currency:primary']),
        ))
        db.send_create_signal('base', ['Currency'])
        
        # Adding model 'CurrencyBase'
        db.create_table('currency_base', (
            ('id', orm['base.CurrencyBase:id']),
            ('name', orm['base.CurrencyBase:name']),
            ('name_small', orm['base.CurrencyBase:name_small']),
            ('code', orm['base.CurrencyBase:code']),
        ))
        db.send_create_signal('base', ['CurrencyBase'])
        
        # Adding model 'NibbleBill'
        db.create_table('nibblebill', (
            ('id', orm['base.NibbleBill:id']),
            ('name', orm['base.NibbleBill:name']),
            ('server', orm['base.NibbleBill:server']),
            ('enabled', orm['base.NibbleBill:enabled']),
        ))
        db.send_create_signal('base', ['NibbleBill'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Balance'
        db.delete_table('balance')
        
        # Deleting model 'Currency'
        db.delete_table('currency')
        
        # Deleting model 'CurrencyBase'
        db.delete_table('currency_base')
        
        # Deleting model 'NibbleBill'
        db.delete_table('nibblebill')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'base.balance': {
            'Meta': {'db_table': "'balance'"},
            'accountcode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contact.Contact']"}),
            'cash': ('CurrencyField', ['_("Balance")'], {'display_decimal': '4', 'max_digits': '18', 'decimal_places': '10'}),
            'credit': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tariff': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tariffplangroup'", 'to': "orm['tariff.TariffPlan']"}),
            'timelimit': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'base.currency': {
            'Meta': {'db_table': "'currency'"},
            'currency_name': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.CurrencyBase']"}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'rate': ('django.db.models.fields.FloatField', [], {'default': '1'})
        },
        'base.currencybase': {
            'Meta': {'db_table': "'currency_base'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_small': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'base.nibblebill': {
            'Meta': {'db_table': "'nibblebill'"},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Server']"})
        },
        'contact.contact': {
            'create_date': ('django.db.models.fields.DateField', [], {}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '500', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contact.Organization']", 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contact.ContactRole']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'contact.contactorganization': {
            'key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'contact.contactorganizationrole': {
            'key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'contact.contactrole': {
            'key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'contact.organization': {
            'create_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contact.ContactOrganizationRole']", 'null': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contact.ContactOrganization']", 'null': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'server.server': {
            'Meta': {'db_table': "'server'"},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listen_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'listen_port': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'sql_login': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'sql_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'sql_password': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'ssh_host': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'ssh_password': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'ssh_user': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'})
        },
        'tariff.tariffplan': {
            'Meta': {'db_table': "'tariff_plan'"},
            'activation': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'cash_min': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '240', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'fee': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'fee_period': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'tariff_format': ('django.db.models.fields.CharField', [], {'default': '"delimiter=\';\'time_format=\'%d.%m.%Y 00:00\'lcr|country_code|special_digits|name|rate"', 'max_length': '250'})
        }
    }
    
    complete_apps = ['base']
