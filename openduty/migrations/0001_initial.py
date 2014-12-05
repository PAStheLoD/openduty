# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Token'
        db.create_table('openduty_token', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('openduty', ['Token'])

        # Adding model 'SchedulePolicy'
        db.create_table('openduty_schedulepolicy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('repeat_times', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('openduty', ['SchedulePolicy'])

        # Adding model 'Service'
        db.create_table('openduty_service', (
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('id', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32, primary_key=True)),
            ('retry', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('policy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openduty.SchedulePolicy'], null=True, blank=True)),
            ('escalate_after', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('openduty', ['Service'])

        # Adding model 'EventLog'
        db.create_table('openduty_eventlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openduty.Service'])),
            ('data', self.gf('django.db.models.fields.TextField')()),
            ('occurred_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('openduty', ['EventLog'])

        # Adding model 'Incident'
        db.create_table('openduty_incident', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openduty.Service'])),
            ('incident_key', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('details', self.gf('django.db.models.fields.TextField')()),
            ('occurred_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('openduty', ['Incident'])

        # Adding unique constraint on 'Incident', fields ['service_key', 'incident_key']
        db.create_unique('openduty_incident', ['service_key_id', 'incident_key'])

        # Adding model 'ServiceTokens'
        db.create_table('openduty_servicetokens', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('service_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openduty.Service'])),
            ('token_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['openduty.Token'])),
        ))
        db.send_create_signal('openduty', ['ServiceTokens'])

        # Adding model 'SchedulePolicyRule'
        db.create_table('openduty_schedulepolicyrule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schedule_policy', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rules', to=orm['openduty.SchedulePolicy'])),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Calendar'], null=True, blank=True)),
            ('escalate_after', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('openduty', ['SchedulePolicyRule'])

        # Adding model 'UserProfile'
        db.create_table('openduty_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pushover_user_key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pushover_app_key', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slack_room_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('openduty', ['UserProfile'])


    def backwards(self, orm):
        # Removing unique constraint on 'Incident', fields ['service_key', 'incident_key']
        db.delete_unique('openduty_incident', ['service_key_id', 'incident_key'])

        # Deleting model 'Token'
        db.delete_table('openduty_token')

        # Deleting model 'SchedulePolicy'
        db.delete_table('openduty_schedulepolicy')

        # Deleting model 'Service'
        db.delete_table('openduty_service')

        # Deleting model 'EventLog'
        db.delete_table('openduty_eventlog')

        # Deleting model 'Incident'
        db.delete_table('openduty_incident')

        # Deleting model 'ServiceTokens'
        db.delete_table('openduty_servicetokens')

        # Deleting model 'SchedulePolicyRule'
        db.delete_table('openduty_schedulepolicyrule')

        # Deleting model 'UserProfile'
        db.delete_table('openduty_userprofile')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'openduty.eventlog': {
            'Meta': {'object_name': 'EventLog'},
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'occurred_at': ('django.db.models.fields.DateTimeField', [], {}),
            'service_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openduty.Service']"})
        },
        'openduty.incident': {
            'Meta': {'unique_together': "(('service_key', 'incident_key'),)", 'object_name': 'Incident'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'details': ('django.db.models.fields.TextField', [], {}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incident_key': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'occurred_at': ('django.db.models.fields.DateTimeField', [], {}),
            'service_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openduty.Service']"})
        },
        'openduty.schedulepolicy': {
            'Meta': {'object_name': 'SchedulePolicy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'repeat_times': ('django.db.models.fields.IntegerField', [], {})
        },
        'openduty.schedulepolicyrule': {
            'Meta': {'object_name': 'SchedulePolicyRule'},
            'escalate_after': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Calendar']", 'null': 'True', 'blank': 'True'}),
            'schedule_policy': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rules'", 'to': "orm['openduty.SchedulePolicy']"}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'openduty.service': {
            'Meta': {'object_name': 'Service'},
            'escalate_after': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'policy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openduty.SchedulePolicy']", 'null': 'True', 'blank': 'True'}),
            'retry': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'openduty.servicetokens': {
            'Meta': {'object_name': 'ServiceTokens'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'service_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openduty.Service']"}),
            'token_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['openduty.Token']"})
        },
        'openduty.token': {
            'Meta': {'object_name': 'Token'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        },
        'openduty.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pushover_app_key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'pushover_user_key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slack_room_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'schedule.calendar': {
            'Meta': {'object_name': 'Calendar'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['openduty']