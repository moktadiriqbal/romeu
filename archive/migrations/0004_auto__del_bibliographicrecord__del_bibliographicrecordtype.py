# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'BibliographicRecord'
        db.delete_table('archive_bibliographicrecord')

        # Deleting model 'BibliographicRecordType'
        db.delete_table('archive_bibliographicrecordtype')

        # Removing M2M table for field secondary_bibliography on 'Production'
        db.delete_table(db.shorten_name('archive_production_secondary_bibliography'))

        # Adding M2M table for field primary_publications on 'Production'
        m2m_table_name = db.shorten_name('archive_production_primary_publications')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm['archive.production'], null=False)),
            ('publication', models.ForeignKey(orm['publications.publication'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'publication_id'])

        # Removing M2M table for field primary_bibliography on 'Creator'
        db.delete_table(db.shorten_name('archive_creator_primary_bibliography'))

        # Removing M2M table for field secondary_bibliography on 'Creator'
        db.delete_table(db.shorten_name('archive_creator_secondary_bibliography'))

        # Adding M2M table for field primary_publications on 'Creator'
        m2m_table_name = db.shorten_name('archive_creator_primary_publications')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('creator', models.ForeignKey(orm['archive.creator'], null=False)),
            ('publication', models.ForeignKey(orm['publications.publication'], null=False))
        ))
        db.create_unique(m2m_table_name, ['creator_id', 'publication_id'])

        # Adding M2M table for field primary_publications on 'WorkRecord'
        m2m_table_name = db.shorten_name('archive_workrecord_primary_publications')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workrecord', models.ForeignKey(orm['archive.workrecord'], null=False)),
            ('publication', models.ForeignKey(orm['publications.publication'], null=False))
        ))
        db.create_unique(m2m_table_name, ['workrecord_id', 'publication_id'])

        # Removing M2M table for field secondary_bibliography on 'FestivalOccurrence'
        db.delete_table(db.shorten_name('archive_festivaloccurrence_secondary_bibliography'))


    def backwards(self, orm):
        # Adding model 'BibliographicRecord'
        db.create_table('archive_bibliographicrecord', (
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('archive_location', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('num_volumes', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('publication', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('booktitle', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('system', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('editor', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('university', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('issue_num', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('library_catalog_num', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('num_pages', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('rights', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('bib_type', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('art_size', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('series', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('library', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('edition', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('access_date', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('archive', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('section', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('tags', self.gf('taggit_autocomplete.managers.TaggableManager')(blank=True)),
            ('translator', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('pages', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('chapter', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('doi', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('issn', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('series_text', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('series_num', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('work_record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['archive.WorkRecord'], null=True, blank=True)),
            ('runtime', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('archive', ['BibliographicRecord'])

        # Adding model 'BibliographicRecordType'
        db.create_table('archive_bibliographicrecordtype', (
            ('has_issue_num', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_pages', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_abstract', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_shorttitle', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_address', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_chapter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_month', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_editor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('has_author', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_year', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('has_workrecord', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_series', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_translator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_edition', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_booktitle', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_volume', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_title', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_url', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_publisher', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_num_volumes', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_pubtitle', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('archive', ['BibliographicRecordType'])

        # Adding M2M table for field secondary_bibliography on 'Production'
        m2m_table_name = db.shorten_name('archive_production_secondary_bibliography')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm['archive.production'], null=False)),
            ('bibliographicrecord', models.ForeignKey(orm['archive.bibliographicrecord'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'bibliographicrecord_id'])

        # Removing M2M table for field primary_publications on 'Production'
        db.delete_table(db.shorten_name('archive_production_primary_publications'))

        # Adding M2M table for field primary_bibliography on 'Creator'
        m2m_table_name = db.shorten_name('archive_creator_primary_bibliography')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('creator', models.ForeignKey(orm['archive.creator'], null=False)),
            ('bibliographicrecord', models.ForeignKey(orm['archive.bibliographicrecord'], null=False))
        ))
        db.create_unique(m2m_table_name, ['creator_id', 'bibliographicrecord_id'])

        # Adding M2M table for field secondary_bibliography on 'Creator'
        m2m_table_name = db.shorten_name('archive_creator_secondary_bibliography')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('creator', models.ForeignKey(orm['archive.creator'], null=False)),
            ('bibliographicrecord', models.ForeignKey(orm['archive.bibliographicrecord'], null=False))
        ))
        db.create_unique(m2m_table_name, ['creator_id', 'bibliographicrecord_id'])

        # Removing M2M table for field primary_publications on 'Creator'
        db.delete_table(db.shorten_name('archive_creator_primary_publications'))

        # Removing M2M table for field primary_publications on 'WorkRecord'
        db.delete_table(db.shorten_name('archive_workrecord_primary_publications'))

        # Adding M2M table for field secondary_bibliography on 'FestivalOccurrence'
        m2m_table_name = db.shorten_name('archive_festivaloccurrence_secondary_bibliography')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('festivaloccurrence', models.ForeignKey(orm['archive.festivaloccurrence'], null=False)),
            ('bibliographicrecord', models.ForeignKey(orm['archive.bibliographicrecord'], null=False))
        ))
        db.create_unique(m2m_table_name, ['festivaloccurrence_id', 'bibliographicrecord_id'])


    models = {
        'archive.advisorymember': {
            'Meta': {'object_name': 'AdvisoryMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.AdvisoryTeamFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Production']"})
        },
        'archive.advisoryteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'AdvisoryTeamFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.award': {
            'Meta': {'object_name': 'Award'},
            'award_org': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'archive.awardcandidate': {
            'Meta': {'object_name': 'AwardCandidate'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'award': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Award']"}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'category_en': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'category_es': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'festival': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'awards'", 'null': 'True', 'to': "orm['archive.Festival']"}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'awards'", 'null': 'True', 'to': "orm['archive.Location']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'awards'", 'null': 'True', 'to': "orm['archive.Production']"}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'awards'", 'null': 'True', 'to': "orm['archive.Creator']"}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'work_record': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'awards'", 'null': 'True', 'to': "orm['archive.WorkRecord']"}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '4'})
        },
        'archive.castmember': {
            'Meta': {'object_name': 'CastMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.CastMemberFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Production']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Role']", 'null': 'True', 'blank': 'True'})
        },
        'archive.castmemberfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'CastMemberFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'to': "orm['archive.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.collection': {
            'Meta': {'object_name': 'Collection'},
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'collection_id': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collections'", 'to': "orm['archive.Repository']"}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'demonym': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'demonym_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'demonym_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.creator': {
            'Meta': {'ordering': "['creator_name']", 'object_name': 'Creator'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'awards_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biography': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biography_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biography_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birth_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'birth_location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'born_here'", 'null': 'True', 'to': "orm['archive.Location']"}),
            'creator_ascii_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creator_display_ascii_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creator_display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creator_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creator_type': ('django.db.models.fields.CharField', [], {'default': "u'person'", 'max_length': '10'}),
            'death_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'death_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'death_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'death_location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'died_here'", 'null': 'True', 'to': "orm['archive.Location']"}),
            'earliest_active': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'earliest_active_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'earliest_active_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "u'N'", 'max_length': '2'}),
            'given_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_active': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'latest_active_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latest_active_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Location']", 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_variants': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nationality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Country']", 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'org_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DigitalObject']", 'null': 'True', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'primary_publications': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'primary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['publications.Publication']"}),
            'profiler_entry_date': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profiler_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'related_creators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['archive.Creator']", 'null': 'True', 'through': "orm['archive.RelatedCreator']", 'blank': 'True'}),
            'secondary_biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.designmember': {
            'Meta': {'object_name': 'DesignMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DesignTeamFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Production']"})
        },
        'archive.designteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'DesignTeamFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.digitalfile': {
            'Meta': {'object_name': 'DigitalFile'},
            'digital_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': "orm['archive.DigitalObject']"}),
            'filepath': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seq_id': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'archive.digitalobject': {
            'Meta': {'object_name': 'DigitalObject'},
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'box_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collection_objects'", 'to': "orm['archive.Collection']"}),
            'creation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'digi_object_format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DigitalObjectType']", 'null': 'True', 'blank': 'True'}),
            'digital_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'donor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'drawer_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'folder_date': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hi_def_video': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'language_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.Language']"}),
            'license_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['archive.License']"}),
            'marks': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'measurements': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'objects_created'", 'null': 'True', 'to': "orm['archive.Creator']"}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'permission_form': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phys_obj_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phys_obj_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'phys_obj_location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Location']", 'null': 'True', 'blank': 'True'}),
            'phys_obj_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'phys_object_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'digital_objects'", 'null': 'True', 'to': "orm['archive.PhysicalObjectType']"}),
            'poster_image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ready_to_stream': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'related_award': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.AwardCandidate']"}),
            'related_creator': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.Creator']"}),
            'related_festival': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.FestivalOccurrence']"}),
            'related_production': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.Production']"}),
            'related_venue': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.Location']"}),
            'related_work': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'related_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.WorkRecord']"}),
            'restricted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'restricted_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'rights_holders': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'series_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'sponsor_note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'collection_objects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.SubjectHeading']"}),
            'subseries_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subseries_num': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        'archive.digitalobjecttype': {
            'Meta': {'object_name': 'DigitalObjectType'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'archive.directingmember': {
            'Meta': {'object_name': 'DirectingMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DirectingTeamFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Production']"})
        },
        'archive.directingteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'DirectingTeamFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.documentationmember': {
            'Meta': {'object_name': 'DocumentationMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DocumentationTeamFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Production']"})
        },
        'archive.documentationteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'DocumentationTeamFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'archive.festival': {
            'Meta': {'object_name': 'Festival'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.festivalfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'FestivalFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.festivaloccurrence': {
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
            'festival_series': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Festival']"}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['archive.Creator']", 'null': 'True', 'through': "orm['archive.FestivalParticipant']", 'blank': 'True'}),
            'productions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archive.Production']", 'symmetrical': 'False'}),
            'profiler_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'program': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archive.Location']", 'symmetrical': 'False'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'archive.festivalparticipant': {
            'Meta': {'object_name': 'FestivalParticipant'},
            'festival': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.FestivalOccurrence']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.FestivalFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"})
        },
        'archive.homepageinfo': {
            'Meta': {'object_name': 'HomePageInfo'},
            'box_1_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'box_2_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'box_3_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_boxes': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        'archive.language': {
            'Meta': {'ordering': "['name']", 'object_name': 'Language'},
            'archival_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'shortcode': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'archive.license': {
            'Meta': {'object_name': 'License'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'more_info_link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'archive.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'altitude': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'begin_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Country']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_venue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locations'", 'null': 'True', 'to': "orm['archive.DigitalObject']"}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'state_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_ascii': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'venue_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.VenueType']", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.orgfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'OrgFunction'},
            'func_type': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.physicalobjecttype': {
            'Meta': {'ordering': "['title']", 'object_name': 'PhysicalObjectType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.production': {
            'Meta': {'object_name': 'Production'},
            'advisory_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'advisory_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.AdvisoryMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'awards_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'begin_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'begin_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1'}),
            'biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cast': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'cast_member_for'", 'symmetrical': 'False', 'through': "orm['archive.CastMember']", 'to': "orm['archive.Creator']"}),
            'design_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'design_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.DesignMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'directing_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'directing_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.DirectingMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'documentation_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'documentation_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.DocumentationMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'end_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'f'", 'max_length': '1'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_special_performance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'num_performances': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'premier': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'primary_publications': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'production_primary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['publications.Publication']"}),
            'production_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'production_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.ProductionMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'profiler_entry_date': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profiler_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'related_organizations': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'productions_related_to'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.Creator']"}),
            'source_work': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'performances'", 'symmetrical': 'False', 'to': "orm['archive.WorkRecord']"}),
            'special_performance_type': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Stage']", 'null': 'True', 'blank': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'technical_team': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'technical_team_for'", 'to': "orm['archive.Creator']", 'through': "orm['archive.TechMember']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'theater_company': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'company_productions'", 'null': 'True', 'to': "orm['archive.Creator']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productions'", 'to': "orm['archive.Location']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.productionmember': {
            'Meta': {'object_name': 'ProductionMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.ProductionTeamFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Production']"})
        },
        'archive.productionteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'ProductionTeamFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.relatedcreator': {
            'Meta': {'object_name': 'RelatedCreator'},
            'first_creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_creator_to'", 'to': "orm['archive.Creator']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.OrgFunction']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'relationship_since': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'relationship_since_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relationship_since_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'relationship_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'relationship_until_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'relationship_until_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'second_creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'second_creator_to'", 'to': "orm['archive.Creator']"})
        },
        'archive.relatedwork': {
            'Meta': {'object_name': 'RelatedWork'},
            'first_work': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_work_to'", 'to': "orm['archive.WorkRecord']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'second_work': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'second_work_to'", 'to': "orm['archive.WorkRecord']"})
        },
        'archive.repository': {
            'Meta': {'object_name': 'Repository'},
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Location']"}),
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
        'archive.role': {
            'Meta': {'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_text': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': "orm['archive.WorkRecord']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'archive.stage': {
            'Meta': {'object_name': 'Stage'},
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stages'", 'to': "orm['archive.Location']"})
        },
        'archive.subjectheading': {
            'Meta': {'object_name': 'SubjectHeading'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_subject': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_subjects'", 'null': 'True', 'to': "orm['archive.SubjectHeading']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'headings'", 'to': "orm['archive.SubjectSource']"}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.subjectsource': {
            'Meta': {'object_name': 'SubjectSource'},
            'ead_title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.techmember': {
            'Meta': {'object_name': 'TechMember'},
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.TechTeamFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Production']"})
        },
        'archive.techteamfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'TechTeamFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.translatingflatpage': {
            'Meta': {'ordering': "('url',)", 'object_name': 'TranslatingFlatPage', '_ormbases': ['flatpages.FlatPage']},
            'child_of': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'flatpage_parent'", 'null': 'True', 'blank': 'True', 'to': "orm['archive.TranslatingFlatPage']"}),
            'content_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'flatpage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['flatpages.FlatPage']", 'unique': 'True', 'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.venuetype': {
            'Meta': {'ordering': "['title']", 'object_name': 'VenueType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'archive.workculture': {
            'Meta': {'object_name': 'WorkCulture'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'archive.workgenre': {
            'Meta': {'object_name': 'WorkGenre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'archive.workrecord': {
            'Meta': {'object_name': 'WorkRecord'},
            'ascii_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'attention': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'awards_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'creators': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['archive.Creator']", 'through': "orm['archive.WorkRecordCreator']", 'symmetrical': 'False'}),
            'creators_display': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'culture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkCulture']", 'null': 'True', 'blank': 'True'}),
            'digital_copy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.DigitalObject']", 'null': 'True', 'blank': 'True'}),
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkGenre']", 'null': 'True', 'blank': 'True'}),
            'has_attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['archive.Language']", 'null': 'True', 'blank': 'True'}),
            'needs_editing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'notes_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'performance_rights': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'performance_rights_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'performance_rights_es': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'primary_publications': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'workedrecord_primary_bibliography_for'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['publications.Publication']"}),
            'publication_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publication_date_BC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publication_date_precision': ('django.db.models.fields.CharField', [], {'default': "u'y'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'publication_rights': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'publication_rights_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'publication_rights_es': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'related_works': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_to'", 'to': "orm['archive.WorkRecord']", 'through': "orm['archive.RelatedWork']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'secondary_biblio_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'secondary_biblio_text_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'style': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkStyle']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'works'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['archive.SubjectHeading']"}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'summary_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_variants': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'work_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkRecordType']"})
        },
        'archive.workrecordcreator': {
            'Meta': {'object_name': 'WorkRecordCreator'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.Creator']"}),
            'function': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkRecordFunction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'work_record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['archive.WorkRecord']"})
        },
        'archive.workrecordfunction': {
            'Meta': {'ordering': "['title']", 'object_name': 'WorkRecordFunction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.workrecordtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'WorkRecordType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_es': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'archive.workstyle': {
            'Meta': {'object_name': 'WorkStyle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'flatpages.flatpage': {
            'Meta': {'ordering': "('url',)", 'object_name': 'FlatPage', 'db_table': "'django_flatpage'"},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'publications.publication': {
            'Meta': {'ordering': "['-year', '-month', '-id']", 'object_name': 'Publication'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_date': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
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
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'how_published': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'pub_date': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'publication': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'tags': ('taggit_autocomplete.managers.TaggableManager', [], {'blank': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['archive']