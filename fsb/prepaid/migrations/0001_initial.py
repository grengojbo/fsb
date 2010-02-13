# -*- mode: python; coding: utf-8; -*-

from south.db import db
from django.db import models
from fsb.prepaid.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Prepaid'
        db.create_table('prepaid_prepaid', (
            ('id', orm['prepaid.Prepaid:id']),
            ('site', orm['prepaid.Prepaid:site']),
            ('num_prepaid', orm['prepaid.Prepaid:num_prepaid']),
            ('code', orm['prepaid.Prepaid:code']),
            ('date_added', orm['prepaid.Prepaid:date_added']),
            ('date_end', orm['prepaid.Prepaid:date_end']),
            ('nt', orm['prepaid.Prepaid:nt']),
            ('enabled', orm['prepaid.Prepaid:enabled']),
            ('valid', orm['prepaid.Prepaid:valid']),
            ('message', orm['prepaid.Prepaid:message']),
            ('start_balance', orm['prepaid.Prepaid:start_balance']),
        ))
        db.send_create_signal('prepaid', ['Prepaid'])
        
        # Creating unique_together for [num_prepaid, code] on Prepaid.
        db.create_unique('prepaid_prepaid', ['num_prepaid', 'code'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [num_prepaid, code] on Prepaid.
        db.delete_unique('prepaid_prepaid', ['num_prepaid', 'code'])
        
        # Deleting model 'Prepaid'
        db.delete_table('prepaid_prepaid')
        
    
    
    models = {
        'prepaid.prepaid': {
            'Meta': {'unique_together': "(('num_prepaid', 'code'),)"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '12', 'unique': 'True'}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'nt': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'max_length': '1'}),
            'num_prepaid': ('django.db.models.fields.CharField', [], {'max_length': '12', 'unique': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'start_balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['prepaid']
