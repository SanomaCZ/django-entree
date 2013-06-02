# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AbstractBaseUser'
        db.create_table('db_abstractbaseuser', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('db', ['AbstractBaseUser'])

        # Deleting field 'EntreeDBUser.last_login'
        db.delete_column(u'db_entreedbuser', 'last_login')

        # Deleting field 'EntreeDBUser.password'
        db.delete_column(u'db_entreedbuser', 'password')

        # Deleting field 'EntreeDBUser.id'
        db.delete_column(u'db_entreedbuser', u'id')

        # Adding field 'EntreeDBUser.abstractbaseuser_ptr'
        db.add_column('db_entreedbuser', 'abstractbaseuser_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['db.AbstractBaseUser'], unique=True, primary_key=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'AbstractBaseUser'
        db.delete_table('db_abstractbaseuser')

        # Adding field 'EntreeDBUser.last_login'
        db.add_column(u'db_entreedbuser', 'last_login',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EntreeDBUser.password'
        raise RuntimeError("Cannot reverse this migration. 'EntreeDBUser.password' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'EntreeDBUser.id'
        raise RuntimeError("Cannot reverse this migration. 'EntreeDBUser.id' and its values cannot be restored.")
        # Deleting field 'EntreeDBUser.abstractbaseuser_ptr'
        db.delete_column('db_entreedbuser', 'abstractbaseuser_ptr_id')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'db.abstractbaseuser': {
            'Meta': {'object_name': 'AbstractBaseUser', '_ormbases': ['auth.User']},
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'db.entreedbuser': {
            'Meta': {'object_name': 'EntreeDBUser', '_ormbases': ['db.AbstractBaseUser']},
            'abstractbaseuser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['db.AbstractBaseUser']", 'unique': 'True', 'primary_key': 'True'}),
            'app_data': ('app_data.fields.AppDataField', [], {'default': "'{}'"}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'})
        }
    }

    complete_apps = ['db']