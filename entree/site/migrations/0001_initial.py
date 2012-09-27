# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SiteProperty'
        db.create_table('site_siteproperty', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.EntreeSite'], blank=True)),
            ('value_type', self.gf('django.db.models.fields.CharField')(default='string', max_length=10)),
            ('is_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_unique', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('site', ['SiteProperty'])

        # Adding unique constraint on 'SiteProperty', fields ['slug', 'site']
        db.create_unique('site_siteproperty', ['slug', 'site_id'])

        # Adding model 'EntreeSite'
        db.create_table('site_entreesite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=150)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('site', ['EntreeSite'])

        # Adding model 'SiteProfile'
        db.create_table('site_siteprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['enauth.Identity'])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.EntreeSite'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('site', ['SiteProfile'])

        # Adding unique constraint on 'SiteProfile', fields ['user', 'site']
        db.create_unique('site_siteprofile', ['user_id', 'site_id'])

        # Adding model 'ProfileDataUnique'
        db.create_table('site_profiledataunique', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['enauth.Identity'])),
            ('site_property', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.SiteProperty'])),
            ('value_int', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('value_str', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
        ))
        db.send_create_signal('site', ['ProfileDataUnique'])

        # Adding unique constraint on 'ProfileDataUnique', fields ['site_property', 'value_str']
        db.create_unique('site_profiledataunique', ['site_property_id', 'value_str'])

        # Adding unique constraint on 'ProfileDataUnique', fields ['site_property', 'value_int']
        db.create_unique('site_profiledataunique', ['site_property_id', 'value_int'])

        # Adding model 'ProfileBigData'
        db.create_table('site_profilebigdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('site', ['ProfileBigData'])

        # Adding model 'ProfileData'
        db.create_table('site_profiledata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['enauth.Identity'])),
            ('site_property', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.SiteProperty'])),
            ('value_int', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('value_str', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('value_big', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['site.ProfileBigData'], null=True)),
            ('value_bool', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('site', ['ProfileData'])


    def backwards(self, orm):
        # Removing unique constraint on 'ProfileDataUnique', fields ['site_property', 'value_int']
        db.delete_unique('site_profiledataunique', ['site_property_id', 'value_int'])

        # Removing unique constraint on 'ProfileDataUnique', fields ['site_property', 'value_str']
        db.delete_unique('site_profiledataunique', ['site_property_id', 'value_str'])

        # Removing unique constraint on 'SiteProfile', fields ['user', 'site']
        db.delete_unique('site_siteprofile', ['user_id', 'site_id'])

        # Removing unique constraint on 'SiteProperty', fields ['slug', 'site']
        db.delete_unique('site_siteproperty', ['slug', 'site_id'])

        # Deleting model 'SiteProperty'
        db.delete_table('site_siteproperty')

        # Deleting model 'EntreeSite'
        db.delete_table('site_entreesite')

        # Deleting model 'SiteProfile'
        db.delete_table('site_siteprofile')

        # Deleting model 'ProfileDataUnique'
        db.delete_table('site_profiledataunique')

        # Deleting model 'ProfileBigData'
        db.delete_table('site_profilebigdata')

        # Deleting model 'ProfileData'
        db.delete_table('site_profiledata')


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
        'site.entreesite': {
            'Meta': {'object_name': 'EntreeSite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '150'})
        },
        'site.profilebigdata': {
            'Meta': {'object_name': 'ProfileBigData'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'site.profiledata': {
            'Meta': {'object_name': 'ProfileData'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site_property': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['site.SiteProperty']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['enauth.Identity']"}),
            'value_big': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['site.ProfileBigData']", 'null': 'True'}),
            'value_bool': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'value_int': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'value_str': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        'site.profiledataunique': {
            'Meta': {'unique_together': "(('site_property', 'value_str'), ('site_property', 'value_int'))", 'object_name': 'ProfileDataUnique'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site_property': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['site.SiteProperty']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['enauth.Identity']"}),
            'value_int': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'value_str': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        'site.siteprofile': {
            'Meta': {'unique_together': "(('user', 'site'),)", 'object_name': 'SiteProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['site.EntreeSite']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['enauth.Identity']"})
        },
        'site.siteproperty': {
            'Meta': {'unique_together': "(('slug', 'site'),)", 'object_name': 'SiteProperty'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_unique': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['site.EntreeSite']", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'value_type': ('django.db.models.fields.CharField', [], {'default': "'string'", 'max_length': '10'})
        }
    }

    complete_apps = ['site']