# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sample'
        db.create_table(u'samples_sample', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=4, primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'samples', ['Sample'])

        # Adding model 'Point'
        db.create_table(u'samples_point', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(srid=900913, blank=True)),
            ('mineral', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('mineral_edited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['samples.Sample'])),
            ('Si', self.gf('django.db.models.fields.FloatField')()),
            ('Fe', self.gf('django.db.models.fields.FloatField')()),
            ('Mg', self.gf('django.db.models.fields.FloatField')()),
            ('Ti', self.gf('django.db.models.fields.FloatField')()),
            ('Al', self.gf('django.db.models.fields.FloatField')()),
            ('Na', self.gf('django.db.models.fields.FloatField')()),
            ('Ca', self.gf('django.db.models.fields.FloatField')()),
            ('Mn', self.gf('django.db.models.fields.FloatField')()),
            ('Cr', self.gf('django.db.models.fields.FloatField')()),
            ('Ni', self.gf('django.db.models.fields.FloatField')()),
            ('Total', self.gf('django.db.models.fields.FloatField')()),
            ('Si_err', self.gf('django.db.models.fields.FloatField')()),
            ('Fe_err', self.gf('django.db.models.fields.FloatField')()),
            ('Mg_err', self.gf('django.db.models.fields.FloatField')()),
            ('Ti_err', self.gf('django.db.models.fields.FloatField')()),
            ('Al_err', self.gf('django.db.models.fields.FloatField')()),
            ('Na_err', self.gf('django.db.models.fields.FloatField')()),
            ('Ca_err', self.gf('django.db.models.fields.FloatField')()),
            ('Mn_err', self.gf('django.db.models.fields.FloatField')()),
            ('Cr_err', self.gf('django.db.models.fields.FloatField')()),
            ('Ni_err', self.gf('django.db.models.fields.FloatField')()),
            ('O', self.gf('django.db.models.fields.IntegerField')()),
            ('SiO2', self.gf('django.db.models.fields.FloatField')()),
            ('FeO', self.gf('django.db.models.fields.FloatField')()),
            ('MgO', self.gf('django.db.models.fields.FloatField')()),
            ('TiO2', self.gf('django.db.models.fields.FloatField')()),
            ('Al2O3', self.gf('django.db.models.fields.FloatField')()),
            ('Na2O', self.gf('django.db.models.fields.FloatField')()),
            ('CaO', self.gf('django.db.models.fields.FloatField')()),
            ('MnO', self.gf('django.db.models.fields.FloatField')()),
            ('Cr2O3', self.gf('django.db.models.fields.FloatField')()),
            ('NiO', self.gf('django.db.models.fields.FloatField')()),
            ('Ox_tot', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'samples', ['Point'])


    def backwards(self, orm):
        # Deleting model 'Sample'
        db.delete_table(u'samples_sample')

        # Deleting model 'Point'
        db.delete_table(u'samples_point')


    models = {
        u'samples.point': {
            'Al': ('django.db.models.fields.FloatField', [], {}),
            'Al2O3': ('django.db.models.fields.FloatField', [], {}),
            'Al_err': ('django.db.models.fields.FloatField', [], {}),
            'Ca': ('django.db.models.fields.FloatField', [], {}),
            'CaO': ('django.db.models.fields.FloatField', [], {}),
            'Ca_err': ('django.db.models.fields.FloatField', [], {}),
            'Cr': ('django.db.models.fields.FloatField', [], {}),
            'Cr2O3': ('django.db.models.fields.FloatField', [], {}),
            'Cr_err': ('django.db.models.fields.FloatField', [], {}),
            'Fe': ('django.db.models.fields.FloatField', [], {}),
            'FeO': ('django.db.models.fields.FloatField', [], {}),
            'Fe_err': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'object_name': 'Point'},
            'Mg': ('django.db.models.fields.FloatField', [], {}),
            'MgO': ('django.db.models.fields.FloatField', [], {}),
            'Mg_err': ('django.db.models.fields.FloatField', [], {}),
            'Mn': ('django.db.models.fields.FloatField', [], {}),
            'MnO': ('django.db.models.fields.FloatField', [], {}),
            'Mn_err': ('django.db.models.fields.FloatField', [], {}),
            'Na': ('django.db.models.fields.FloatField', [], {}),
            'Na2O': ('django.db.models.fields.FloatField', [], {}),
            'Na_err': ('django.db.models.fields.FloatField', [], {}),
            'Ni': ('django.db.models.fields.FloatField', [], {}),
            'NiO': ('django.db.models.fields.FloatField', [], {}),
            'Ni_err': ('django.db.models.fields.FloatField', [], {}),
            'O': ('django.db.models.fields.IntegerField', [], {}),
            'Ox_tot': ('django.db.models.fields.FloatField', [], {}),
            'Si': ('django.db.models.fields.FloatField', [], {}),
            'SiO2': ('django.db.models.fields.FloatField', [], {}),
            'Si_err': ('django.db.models.fields.FloatField', [], {}),
            'Ti': ('django.db.models.fields.FloatField', [], {}),
            'TiO2': ('django.db.models.fields.FloatField', [], {}),
            'Ti_err': ('django.db.models.fields.FloatField', [], {}),
            'Total': ('django.db.models.fields.FloatField', [], {}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '900913', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'mineral': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'mineral_edited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['samples.Sample']"})
        },
        u'samples.sample': {
            'Meta': {'object_name': 'Sample'},
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'})
        }
    }

    complete_apps = ['samples']