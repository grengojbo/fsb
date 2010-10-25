# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Balance'
        db.create_table('balance', (
            ('accountcode', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('cash', self.gf('bursar.fields.CurrencyField')(default='0.00', max_digits=18, decimal_places=2)),
            ('tariff', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='tariffplangroup', to=orm['tariff.TariffPlan'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('timelimit', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('credit', self.gf('bursar.fields.CurrencyField')(default='0.0', max_digits=8, decimal_places=2)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site'])),
        ))
        db.send_create_signal('billing', ['Balance'])

        # Adding model 'BalanceHistory'
        db.create_table('balance_history', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('amount', self.gf('bursar.fields.CurrencyField')(null=True, max_digits=18, decimal_places=2, blank=True)),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('transaction_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=45)),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('reason_code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('accountcode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Balance'])),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site'])),
            ('pay_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2010, 10, 21, 15, 23, 49, 117011))),
        ))
        db.send_create_signal('billing', ['BalanceHistory'])

        # Adding model 'CreditBase'
        db.create_table('balance_credit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('balance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['billing.Balance'])),
            ('credit', self.gf('django.db.models.fields.DecimalField')(default='0.0', max_digits=18, decimal_places=2)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('time_stamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('expire_time', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
        ))
        db.send_create_signal('billing', ['CreditBase'])


    def backwards(self, orm):
        
        # Deleting model 'Balance'
        db.delete_table('balance')

        # Deleting model 'BalanceHistory'
        db.delete_table('balance_history')

        # Deleting model 'CreditBase'
        db.delete_table('balance_credit')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'billing.balance': {
            'Meta': {'object_name': 'Balance', 'db_table': "'balance'"},
            'accountcode': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'cash': ('bursar.fields.CurrencyField', [], {'default': "'0.00'", 'max_digits': '18', 'decimal_places': '2'}),
            'credit': ('bursar.fields.CurrencyField', [], {'default': "'0.0'", 'max_digits': '8', 'decimal_places': '2'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}),
            'tariff': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'tariffplangroup'", 'to': "orm['tariff.TariffPlan']"}),
            'timelimit': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'billing.balancehistory': {
            'Meta': {'object_name': 'BalanceHistory', 'db_table': "'balance_history'"},
            'accountcode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Balance']"}),
            'amount': ('bursar.fields.CurrencyField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '2', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pay_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 21, 15, 23, 49, 117011)'}),
            'reason_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '45'})
        },
        'billing.creditbase': {
            'Meta': {'object_name': 'CreditBase', 'db_table': "'balance_credit'"},
            'balance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['billing.Balance']"}),
            'credit': ('django.db.models.fields.DecimalField', [], {'default': "'0.0'", 'max_digits': '18', 'decimal_places': '2'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'expire_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_stamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'tariff.tariffplan': {
            'Meta': {'ordering': "['-primary']", 'object_name': 'TariffPlan', 'db_table': "'tariff_plan'"},
            'activation': ('bursar.fields.CurrencyField', [], {'default': "'0.00'", 'max_digits': '18', 'decimal_places': '2'}),
            'cash_min': ('bursar.fields.CurrencyField', [], {'default': "'0.00'", 'max_digits': '18', 'decimal_places': '2'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2010, 10, 21, 15, 23, 49, 579)'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '240', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fee': ('bursar.fields.CurrencyField', [], {'default': "'0.00'", 'max_digits': '18', 'decimal_places': '2'}),
            'fee_period': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"})
        }
    }

    complete_apps = ['billing']
