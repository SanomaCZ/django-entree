# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LoginToken'
        db.create_table('enauth_logintoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['enauth.Identity'])),
            ('value', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('token_type', self.gf('django.db.models.fields.CharField')(default='AUTH', max_length=5, db_index=True)),
            ('extra_data', self.gf('jsonfield.fields.JSONField')(default='{}', blank=True)),
            ('touched', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('enauth', ['LoginToken'])

        # Adding model 'Identity'
        db.create_table('enauth_identity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('mail_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('enauth', ['Identity'])


    def backwards(self, orm):
        # Deleting model 'LoginToken'
        db.delete_table('enauth_logintoken')

        # Deleting model 'Identity'
        db.delete_table('enauth_identity')


    models = {
        'enauth.identity': {
            'Meta': {'object_name': 'Identity'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mail_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'enauth.logintoken': {
            'Meta': {'object_name': 'LoginToken'},
            'extra_data': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token_type': ('django.db.models.fields.CharField', [], {'default': "'AUTH'", 'max_length': '5', 'db_index': 'True'}),
            'touched': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['enauth.Identity']"}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        }
    }

    complete_apps = ['enauth']