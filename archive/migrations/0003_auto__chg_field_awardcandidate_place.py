# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field secondary_publications on 'Production'
        m2m_table_name = db.shorten_name(u'archive_production_secondary_publications')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm[u'archive.production'], null=False)),
            ('publication', models.ForeignKey(orm['publications.publication'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'publication_id'])


        # Changing field 'AwardCandidate.place'
        db.alter_column(u'archive_awardcandidate', 'place_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['archive.City']))
        # Adding M2M table for field secondary_publications on 'Creator'
        m2m_table_name = db.shorten_name(u'archive_creator_secondary_publications')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('creator', models.ForeignKey(orm[u'archive.creator'], null=False)),
            ('publication', models.ForeignKey(orm['publications.publication'], null=False))
        ))
        db.create_unique(m2m_table_name, ['creator_id', 'publication_id'])

        # Adding M2M table for field secondary_publications on 'WorkRecord'
        m2m_table_name = db.shorten_name(u'archive_workrecord_secondary_publications')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workrecord', models.ForeignKey(orm[u'archive.workrecord'], null=False)),
            ('publication', models.ForeignKey(orm['publications.publication'], null=False))
        ))
        db.create_unique(m2m_table_name, ['workrecord_id', 'publication_id'])


    def backwards(self, orm):
        # Removing M2M table for field secondary_publications on 'Production'
        db.delete_table(db.shorten_name(u'archive_production_secondary_publications'))


        # Changing field 'AwardCandidate.place'
        db.alter_column(u'archive_awardcandidate', 'place_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['archive.Location']))
        # Removing M2M table for field secondary_publications on 'Creator'
        db.delete_table(db.shorten_name(u'archive_creator_secondary_publications'))

        # Removing M2M table for field secondary_publications on 'WorkRecord'
        db.delete_table(db.shorten_name(u'archive_workrecord_secondary_publications'))


    models = {
        u'archive.advisorymember': {
            'Meta': {'object_name': 'AdvisoryMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.AdvisoryTeamFunction']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Production']"})
        },
        u'archive.advisoryteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'AdvisoryTeamFunction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'archive.award': {
            'Meta': {'ordering': "['title']", 'object_name': 'Award'},
            'award_org': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'archive.awardcandidate': {
            'Meta': {'ordering': "['award', 'year']", 'object_name': 'AwardCandidate'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'award': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Award']"}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'category_en': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'category_es': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'festival': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'festival'", 'null': 'True', 'blank': 'True', 'to': u"orm['archive.Festival']"}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'place'", 'null': 'True', 'blank': 'True', 'to': u"orm['archive.City']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'production'", 'null': 'True', 'blank': 'True', 'to': u"orm['archive.Production']"}),
            'profiler_entry_date': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profiler_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'recipient'", 'null': 'True', 'to': u"orm['archive.Creator']"}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'work_record': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'work_record'", 'null': 'True', 'blank': 'True', 'to': u"orm['archive.WorkRecord']"}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '4'})
        },
        u'archive.castmember': {
            'Meta': {'object_name': 'CastMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.CastMemberFunction']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Production']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['archive.Role']", 'null': 'True', 'blank': 'True'})
        },
        u'archive.castmemberfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'CastMemberFunction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'archive.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'to': u"orm['archive.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'archive.collection': {
            'Meta': {'object_name': 'Collection'},
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collection_id': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collections'", 'to': u"orm['archive.Repository']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'archive.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'demonym': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'demonym_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'demonym_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'archive.creator': {
            'Meta': {'ordering': "['creator_name']", 'object_name': 'Creator'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'awards_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biography': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biography_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biography_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birth_city': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'born_here'", 'null': 'True', 'to': u"orm['archive.City']"}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birth_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'birth_location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'born_here'", 'null': 'True', 'to': u"orm['archive.Location']"}),
            'creator_ascii_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creator_display_ascii_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creator_display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creator_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creator_type': ('django.db.models.fields.CharField', [], {'default': "u'person'", 'max_length': '10'}),
            'death_city': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'died_here'", 'null': 'True', 'to': u"orm['archive.City']"}),
            'death_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'death_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'death_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'death_location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'died_here'", 'null': 'True', 'to': u"orm['archive.Location']"}),
            'earliest_active': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'earliest_active_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'earliest_active_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "u'N'", 'max_length': '2'}),
            'given_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'headquarter_city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.City']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_active': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'latest_active_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latest_active_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Location']", 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_variants': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nationality': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Country']", 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'org_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.DigitalObject']", 'null': 'True', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'primary_publications': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'primary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['publications.Publication']"}),
            'profiler_entry_date': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profiler_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'related_creators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['archive.Creator']", 'null': 'True', 'through': u"orm['archive.RelatedCreator']", 'blank': 'True'}),
            'secondary_biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_publications': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'secondary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['publications.Publication']"}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'archive.designmember': {
            'Meta': {'object_name': 'DesignMember'},
            'functions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'functions'", 'symmetrical': 'False', 'to': u"orm['archive.DesignTeamFunction']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Production']"})
        },
        u'archive.designteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'DesignTeamFunction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'archive.digitalfile': {
            'Meta': {'object_name': 'DigitalFile'},
            'digital_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': u"orm['archive.DigitalObject']"}),
            'filepath': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seq_id': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        u'archive.digitalobject': {
            'Meta': {'ordering': "['-collection__repository__repository_id', '-collection__collection_id', '-object_id']", 'object_name': 'DigitalObject'},
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'box_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collection_objects'", 'to': u"orm['archive.Collection']"}),
            'creation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'digi_object_format': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.DigitalObjectType']", 'null': 'True', 'blank': 'True'}),
            'digital_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'donor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'drawer_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'folder_date': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hi_def_video': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'language_objects'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['archive.Language']"}),
            'license_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['archive.License']"}),
            'marks': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'measurements': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'objects_created'", 'null': 'True', 'to': u"orm['archive.Creator']"}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'permission_form': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phys_obj_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phys_obj_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'phys_obj_location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Location']", 'null': 'True', 'blank': 'True'}),
            'phys_obj_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'phys_object_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'digital_objects'", 'null': 'True', 'to': u"orm['archive.PhysicalObjectType']"}),
            'poster_image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ready_to_stream': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'related_award': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_award'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['archive.AwardCandidate']"}),
            'related_creator': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_creator'", 'to': u"orm['archive.Creator']", 'through': u"orm['archive.DigitalObject_Related_Creator']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'related_festival': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_festival'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['archive.FestivalOccurrence']"}),
            'related_production': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_production'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['archive.Production']"}),
            'related_venue': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_venue'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['archive.Location']"}),
            'related_work': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_work'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['archive.WorkRecord']"}),
            'restricted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'restricted_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'rights_holders': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'sponsor_note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'collection_objects'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['archive.SubjectHeading']"}),
            'subseries_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subseries_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'title_variants_en': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'title_variants_es': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        u'archive.digitalobject_related_creator': {
            'Meta': {'object_name': 'DigitalObject_Related_Creator'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Creator']"}),
            'digitalobject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.DigitalObject']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'archive.digitalobjecttype': {
            'Meta': {'object_name': 'DigitalObjectType'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'archive.directingmember': {
            'Meta': {'object_name': 'DirectingMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.DirectingTeamFunction']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Production']"})
        },
        u'archive.directingteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'DirectingTeamFunction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'archive.documentationmember': {
            'Meta': {'object_name': 'DocumentationMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.DocumentationTeamFunction']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Production']"})
        },
        u'archive.documentationteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'DocumentationTeamFunction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'archive.festival': {
            'Meta': {'object_name': 'Festival'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'archive.festivalfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'FestivalFunction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'archive.festivaloccurrence': {
            'Meta': {'object_name': 'FestivalOccurrence'},
            'announcement': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'awards_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {}),
            'begin_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'begin_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1'}),
            'edu_program': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'end_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1'}),
            'festival_series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Festival']"}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['archive.Creator']", 'null': 'True', 'through': u"orm['archive.FestivalParticipant']", 'blank': 'True'}),
            'primary_publications': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'festival_primary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['publications.Publication']"}),
            'productions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['archive.Production']", 'symmetrical': 'False'}),
            'profiler_entry_date': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profiler_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'program': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['archive.Location']", 'symmetrical': 'False'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'archive.festivalparticipant': {
            'Meta': {'object_name': 'FestivalParticipant'},
            'festival': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.FestivalOccurrence']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.FestivalFunction']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Creator']"})
        },
        u'archive.homepageinfo': {
            'Meta': {'object_name': 'HomePageInfo'},
            'box_1_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'box_2_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'box_3_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_boxes': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        u'archive.language': {
            'Meta': {'ordering': "['name']", 'object_name': 'Language'},
            'archival_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'shortcode': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'archive.license': {
            'Meta': {'object_name': 'License'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'more_info_link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'archive.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'altitude': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'begin_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Country']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_venue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locations'", 'null': 'True', 'to': u"orm['archive.DigitalObject']"}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'profiler_entry_date': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profiler_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_ascii': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'venue_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.VenueType']", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'archive.orgfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'OrgFunction'},
            'func_type': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordinal': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'archive.physicalobjecttype': {
            'Meta': {'ordering': "['title']", 'object_name': 'PhysicalObjectType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'archive.production': {
            'Meta': {'ordering': "['title']", 'object_name': 'Production'},
            'advisory_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'advisory_team_for'", 'to': u"orm['archive.Creator']", 'through': u"orm['archive.AdvisoryMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'awards_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'begin_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1'}),
            'biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cast': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'cast_member_for'", 'symmetrical': 'False', 'through': u"orm['archive.CastMember']", 'to': u"orm['archive.Creator']"}),
            'design_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'design_team_for'", 'to': u"orm['archive.Creator']", 'through': u"orm['archive.DesignMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'directing_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'directing_team_for'", 'to': u"orm['archive.Creator']", 'through': u"orm['archive.DirectingMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'documentation_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'documentation_team_for'", 'to': u"orm['archive.Creator']", 'through': u"orm['archive.DocumentationMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_special_performance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'num_performances': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'premier': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'primary_publications': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'production_primary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['publications.Publication']"}),
            'production_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'production_team_for'", 'to': u"orm['archive.Creator']", 'through': u"orm['archive.ProductionMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'profiler_entry_date': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profiler_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'related_organizations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'productions_related_to'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['archive.Creator']"}),
            'secondary_publications': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'production_secondary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['publications.Publication']"}),
            'source_work': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'performances'", 'symmetrical': 'False', 'to': u"orm['archive.WorkRecord']"}),
            'special_performance_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'special_performance_type'", 'null': 'True', 'blank': 'True', 'to': u"orm['archive.SpecialPerformanceType']"}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Stage']", 'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'technical_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'technical_team_for'", 'to': u"orm['archive.Creator']", 'through': u"orm['archive.TechMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'theater_companies': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'company_productions'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['archive.Creator']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productions'", 'to': u"orm['archive.Location']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'archive.productionmember': {
            'Meta': {'object_name': 'ProductionMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.ProductionTeamFunction']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Production']"})
        },
        u'archive.productionteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'ProductionTeamFunction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'archive.relatedcreator': {
            'Meta': {'object_name': 'RelatedCreator'},
            'first_creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_creator_to'", 'to': u"orm['archive.Creator']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.OrgFunction']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'relationship_since': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'relationship_since_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relationship_since_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'relationship_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'relationship_until_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relationship_until_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'second_creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'second_creator_to'", 'to': u"orm['archive.Creator']"})
        },
        u'archive.relatedwork': {
            'Meta': {'object_name': 'RelatedWork'},
            'first_work': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_work_to'", 'to': u"orm['archive.WorkRecord']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'second_work': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'second_work_to'", 'to': u"orm['archive.WorkRecord']"})
        },
        u'archive.repository': {
            'Meta': {'object_name': 'Repository'},
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Location']"}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'repository_id': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'archive.role': {
            'Meta': {'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_text': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': u"orm['archive.WorkRecord']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'archive.specialperformancetype': {
            'Meta': {'ordering': "['type']", 'object_name': 'SpecialPerformanceType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'type_en': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'type_es': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'})
        },
        u'archive.stage': {
            'Meta': {'object_name': 'Stage'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'seating': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'square_footage': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stage_depth': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stage_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stage_lighting': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stage_lighting_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stage_lighting_es': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stage_sound': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stage_sound_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stage_sound_es': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stage_type': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'stage_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stages'", 'to': u"orm['archive.Location']"})
        },
        u'archive.subjectheading': {
            'Meta': {'object_name': 'SubjectHeading'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_subject': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_subjects'", 'null': 'True', 'to': u"orm['archive.SubjectHeading']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'headings'", 'to': u"orm['archive.SubjectSource']"}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'archive.subjectsource': {
            'Meta': {'object_name': 'SubjectSource'},
            'ead_title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'archive.techmember': {
            'Meta': {'object_name': 'TechMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.TechTeamFunction']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Production']"})
        },
        u'archive.techteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'TechTeamFunction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'archive.translatingflatpage': {
            'Meta': {'ordering': "(u'url',)", 'object_name': 'TranslatingFlatPage', '_ormbases': [u'flatpages.FlatPage']},
            'child_of': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'flatpage_parent'", 'null': 'True', 'blank': 'True', 'to': u"orm['archive.TranslatingFlatPage']"}),
            'content_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'flatpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['flatpages.FlatPage']", 'unique': 'True', 'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'archive.venuetype': {
            'Meta': {'ordering': "['title']", 'object_name': 'VenueType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'archive.workculture': {
            'Meta': {'object_name': 'WorkCulture'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'archive.workgenre': {
            'Meta': {'object_name': 'WorkGenre'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'archive.workrecord': {
            'Meta': {'ordering': "['title']", 'object_name': 'WorkRecord'},
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'awards_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'creators': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['archive.Creator']", 'through': u"orm['archive.WorkRecordCreator']", 'symmetrical': 'False'}),
            'creators_display': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'culture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.WorkCulture']", 'null': 'True', 'blank': 'True'}),
            'digital_copy': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.DigitalObject']", 'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.WorkGenre']", 'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['archive.Language']", 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'performance_rights': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'performance_rights_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'performance_rights_es': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'primary_publications': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'workedrecord_primary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['publications.Publication']"}),
            'profiler_entry_date': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profiler_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publication_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publication_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'publication_rights': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publication_rights_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'publication_rights_es': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'related_works': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_to'", 'to': u"orm['archive.WorkRecord']", 'through': u"orm['archive.RelatedWork']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'secondary_biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_publications': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'workedrecord_secondary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['publications.Publication']"}),
            'style': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.WorkStyle']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'works'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['archive.SubjectHeading']"}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'work_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.WorkRecordType']"})
        },
        u'archive.workrecordcreator': {
            'Meta': {'object_name': 'WorkRecordCreator'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.Creator']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.WorkRecordFunction']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'work_record': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['archive.WorkRecord']"})
        },
        u'archive.workrecordfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'WorkRecordFunction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'archive.workrecordtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'WorkRecordType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'archive.workstyle': {
            'Meta': {'object_name': 'WorkStyle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'flatpages.flatpage': {
            'Meta': {'ordering': "(u'url',)", 'object_name': 'FlatPage', 'db_table': "u'django_flatpage'"},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'publications.publication': {
            'Meta': {'ordering': "['-year', '-month', '-id']", 'object_name': 'Publication'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'annote': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'archive': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'archive_location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'art_size': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'authors': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'book_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'chapter': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'citekey': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'how_published': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'issn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'library': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'library_catalog_num': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'rights': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'runtime': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series_num': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'series_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'system': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'table_of_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'translator': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['publications.Type']"}),
            'university': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '4'})
        },
        'publications.type': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Type'},
            'bibtex_types': ('django.db.models.fields.CharField', [], {'default': "'article'", 'max_length': '256'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['archive']