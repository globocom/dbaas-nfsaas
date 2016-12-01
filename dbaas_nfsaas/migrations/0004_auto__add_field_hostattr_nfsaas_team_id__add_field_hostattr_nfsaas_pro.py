# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from os.path import abspath, dirname


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'HostAttr.nfsaas_team_id'
        db.add_column(u'dbaas_nfsaas_hostattr', 'nfsaas_team_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10),
                      keep_default=False)

        # Adding field 'HostAttr.nfsaas_project_id'
        db.add_column(u'dbaas_nfsaas_hostattr', 'nfsaas_project_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10),
                      keep_default=False)

        # Adding field 'HostAttr.nfsaas_environment_id'
        db.add_column(u'dbaas_nfsaas_hostattr', 'nfsaas_environment_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10),
                      keep_default=False)

        # Adding field 'HostAttr.nfsaas_size_id'
        db.add_column(u'dbaas_nfsaas_hostattr', 'nfsaas_size_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10),
                      keep_default=False)

        sql_migration_file = "{}/migration_0004_up.sql".format(abspath(dirname(__file__)))
        db.execute(open(sql_migration_file).read())


    def backwards(self, orm):
        # Deleting field 'HostAttr.nfsaas_team_id'
        db.delete_column(u'dbaas_nfsaas_hostattr', 'nfsaas_team_id')

        # Deleting field 'HostAttr.nfsaas_project_id'
        db.delete_column(u'dbaas_nfsaas_hostattr', 'nfsaas_project_id')

        # Deleting field 'HostAttr.nfsaas_environment_id'
        db.delete_column(u'dbaas_nfsaas_hostattr', 'nfsaas_environment_id')

        # Deleting field 'HostAttr.nfsaas_size_id'
        db.delete_column(u'dbaas_nfsaas_hostattr', 'nfsaas_size_id')


    models = {
        u'dbaas_nfsaas.environmentattr': {
            'Meta': {'object_name': 'EnvironmentAttr'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dbaas_environment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nfsaas_environment_attributes'", 'to': u"orm['physical.Environment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nfsaas_environment': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'dbaas_nfsaas.hostattr': {
            'Meta': {'object_name': 'HostAttr'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nfsaas_host_attributes'", 'to': u"orm['physical.Host']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nfsaas_environment_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'nfsaas_export_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'nfsaas_path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'nfsaas_project_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'nfsaas_size_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'nfsaas_team_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'dbaas_nfsaas.planattr': {
            'Meta': {'object_name': 'PlanAttr'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dbaas_plan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nfsaas_plan_attributes'", 'to': u"orm['physical.Plan']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nfsaas_plan': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'physical.enginetype': {
            'Meta': {'object_name': 'EngineType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'physical.environment': {
            'Meta': {'object_name': 'Environment'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'equivalent_environment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['physical.Environment']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'physical.host': {
            'Meta': {'object_name': 'Host'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'future_host': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['physical.Host']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monitor_url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'physical.plan': {
            'Meta': {'object_name': 'Plan'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'engine_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'plans'", 'to': u"orm['physical.EngineType']"}),
            'environments': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['physical.Environment']", 'symmetrical': 'False'}),
            'equivalent_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['physical.Plan']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_ha': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_db_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'provider': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['dbaas_nfsaas']
