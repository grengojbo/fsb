# -*- mode: python; coding: utf-8; -*-

from south.db import db
from django.db import models
from fsb.prepaid.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Deleting field 'Prepaid.site'
        db.delete_column('prepaid_prepaid', 'site_id')
        
    
    
    def backwards(self, orm):
        
        # Adding field 'Prepaid.site'
        db.add_column('prepaid_prepaid', 'site', orm['prepaid.prepaid:site'])
        
    
    
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
            'start_balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        }
    }
    
    complete_apps = ['prepaid']
