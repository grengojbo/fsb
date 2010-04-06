# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Prepaid'
        db.create_table('prepaid_prepaid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num_prepaid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=12)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=12)),
            ('date_added', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('date_end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('nt', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, max_length=1)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('start_balance', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('prepaid', ['Prepaid'])

        # Adding unique constraint on 'Prepaid', fields ['num_prepaid', 'code']
        db.create_unique('prepaid_prepaid', ['num_prepaid', 'code'])


    def backwards(self, orm):
        
        # Deleting model 'Prepaid'
        db.delete_table('prepaid_prepaid')

        # Removing unique constraint on 'Prepaid', fields ['num_prepaid', 'code']
        db.delete_unique('prepaid_prepaid', ['num_prepaid', 'code'])


    models = {
        'prepaid.prepaid': {
            'Meta': {'unique_together': "(('num_prepaid', 'code'),)", 'object_name': 'Prepaid'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'nt': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'max_length': '1'}),
            'num_prepaid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'start_balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['prepaid']
