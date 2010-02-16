# -*- mode: python; coding: utf-8; -*-

from south.db import db
from django.db import models
from fsb.billing.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'CreditBase.user'
        db.add_column('billing_creditbase', 'user', orm['billing.creditbase:user'])
        
        # Deleting field 'CreditBase.usere'
        db.delete_column('billing_creditbase', 'usere_id')
        
        # Changing field 'CreditBase.credit'
        # (to signature: django.db.models.fields.DecimalField(max_digits=18, decimal_places=2))
        db.alter_column('billing_creditbase', 'credit', orm['billing.creditbase:credit'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'CreditBase.user'
        db.delete_column('billing_creditbase', 'user_id')
        
        # Adding field 'CreditBase.usere'
        db.add_column('billing_creditbase', 'usere', orm['billing.creditbase:usere'])
        
        # Changing field 'CreditBase.credit'
        # (to signature: django.db.models.fields.DecimalField(max_digits=18, decimal_places=10))
        db.alter_column('billing_creditbase', 'credit', orm['billing.creditbase:credit'])
        
    
    
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
        'billing.balance': {
            'Meta': {'db_table': "'balance'"},
            'accountcode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'cash': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '2'}),
            'credit': ('django.db.models.fields.DecimalField', [], {'default': 'Decimal("0.0")', 'max_digits': '18', 'decimal_places': '2'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timelimit': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'billing.balancehistory': {
            'Meta': {'db_table': "'balance_history'"},
            'accountcode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'cash': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '2'}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'billing.creditbase': {
            'balance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Balance']"}),
            'credit': ('django.db.models.fields.DecimalField', [], {'default': 'Decimal("0.0")', 'max_digits': '18', 'decimal_places': '2'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'expire_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['billing']
