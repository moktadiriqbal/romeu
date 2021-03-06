
"""
    # Copyright (C) 2012  University of Miami
    #
    # This program is free software; you can redistribute it and/or
    # modify it under the terms of the GNU General Public License
    # as published by the Free Software Foundation; either version 2
    # of the License, or (at your option) any later version.
    #
    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    # See the GNU General Public License for more details.
    #
    # You should have received a copy of the GNU General Public License
    # along with this program; if not, write to the Free Software Foundation,
    # Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

    # coding: utf-8
"""

import os

from django.contrib.auth import models as auth_models
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.core.files.storage import FileSystemStorage

from django.db.models import Q
from django.db import models
from django.db.models import Min, Max, Avg, Count
from django.db.models.signals import pre_save, post_save, post_delete

from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from unidecode import unidecode

from smart_selects.db_fields import ChainedForeignKey
from publications.models.publication import Publication
from publications.fields import PagesField
from archive.utils import display_date
from archive import constants

# import reversion

from random import choice, shuffle

from taggit_autocomplete_modified.managers import TaggableManager

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([((TaggableManager, ), [], {}, ),
        ((PagesField,), [], {}, )],
        ["^taggit_autocomplete_modified\.managers\.TaggableManager",
         "^publications\.fields\.PagesField", ])
except ImportError:
    pass

class SpecialPerformanceType(models.Model):
    type = models.CharField(max_length=24, verbose_name=_("Type"))

    class Meta:
        verbose_name = _("special performance type")
        verbose_name_plural = _("special performance types")
        ordering = ['type']

    def __unicode__(self):
        return self.type

class OverwriteStorage(FileSystemStorage):
    """
    Returns same name for existing file and deletes existing file on save.
    """
    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name):
        return name

def check_attention(sender, **kwargs):
    obj = kwargs['instance']
    try:
        if obj.attention == None or obj.attention == u'':
            att = False
        else:
            att = True
        obj.has_attention = att
    except:
        pass
pre_save.connect(check_attention)


def make_unique(seq, idfun=None):
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

# Subject heading models
class SubjectSource(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    ead_title = models.CharField(max_length=50, verbose_name=_("EAD title"))

    def __unicode__(self):
        return self.title

class SubjectHeading(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name=_("title"))
    subject_type = models.CharField(max_length=10,
                                    choices=constants.SUBJECT_TYPE_CHOICES,
                                    verbose_name=_("subject type"))
    source = models.ForeignKey(SubjectSource,
                               related_name="headings",
                               verbose_name=_("source"))
    parent_subject = models.ForeignKey("self", null=True, blank=True,
                                       related_name="child_subjects",
                                       verbose_name=_("parent subject"))
    def __unicode__(self):
        return "%s (%s)" % (self.title, self.get_subject_type_display())

class Creator(models.Model):
    creator_type = models.CharField(max_length=10,
                                    choices=constants.CREATOR_TYPE_CHOICES,
                                    default=u'person',
                                    verbose_name=_("creator type"))
    prefix = models.CharField(max_length=100, null=True, blank=True,
                              verbose_name=_("name prefix"))
    given_name = models.CharField(max_length=255, null=True, blank=True,
                                  verbose_name=_("given name(s)"))
    middle_name = models.CharField(max_length=255, null=True, blank=True,
                                   verbose_name=_("middle name(s)"))
    family_name = models.CharField(max_length=255, null=True, blank=True,
                                   verbose_name=_("family name(s)"))
    suffix = models.CharField(max_length=100, null=True, blank=True,
                              verbose_name=_("name suffix"))
    org_name = models.CharField(max_length=255, null=True, blank=True,
                                help_text=_("For corporate creators, \
                                            enter an organization name here \
                                            instead of using the other \
                                            name fields."),
                                verbose_name=_("organization / corporate name")
                                )
    creator_name = models.CharField(max_length=255,
                                    verbose_name=_("creator name"))
    creator_ascii_name = models.CharField(max_length=255,
                                          verbose_name=_("creator ASCII name"))
    creator_display_name = models.CharField(max_length=255,
                                            verbose_name=_("creator display name"))
    creator_display_ascii_name = models.CharField(
        max_length=255,verbose_name=_("creator display ASCII name"))
    name_variants = models.CharField(max_length=200, null=True, blank=True,
                                     verbose_name=_("name variants"))
    birth_city = models.ForeignKey("City", null=True, blank=True,
                                   related_name="born_here",
                                   verbose_name=_("City of birth"))
    birth_date = models.DateField(null=True, blank=True,
                                  help_text="Click 'Today' to see today's date \
                                            in the proper date format.",
                                  verbose_name=_("birth date"))
    birth_date_precision = models.CharField(
        max_length=1,
        choices=constants.DATE_PRECISION_CHOICES,
        default=u'f',
        null=True, blank=True,
        verbose_name=_("Precision"))
    birth_date_BC = models.BooleanField(default=False,
                                        verbose_name=_("Is B.C. date"))
    death_city = models.ForeignKey("City", null=True, blank=True,
                                   related_name="died_here",
                                   verbose_name=_("City of death"))
    death_date = models.DateField(null=True, blank=True,
                                  help_text="Click 'Today' to see today's date \
                                            in the proper date format.",
                                  verbose_name=_("death date"))
    death_date_precision = models.CharField(
        max_length=1,
        choices=constants.DATE_PRECISION_CHOICES,
        default=u'f', null=True, blank=True,
        verbose_name=_("Precision"))
    death_date_BC = models.BooleanField(default=False,
                                        verbose_name=_("Is B.C. date"))
    earliest_active = models.DateField(
        null=True, blank=True,
        help_text="Click 'Today' to see today's \
                  date in the proper date format.",
        verbose_name=_("earliest active"))
    earliest_active_precision = models.CharField(
        max_length=1,
        choices=constants.DATE_PRECISION_CHOICES,
        default=u'y', null=True, blank=True,
        verbose_name=_("Precision"))
    earliest_active_BC = models.BooleanField(default=False,
                                             verbose_name=_("Is B.C. date"))
    latest_active = models.DateField(
        null=True, blank=True,
        help_text="Click 'Today' to see today's \
                  date in the proper date format.",
        verbose_name=_("latest active"))
    latest_active_precision = models.CharField(
        max_length=1,
        choices=constants.DATE_PRECISION_CHOICES,
        default=u'y', null=True, blank=True,
        verbose_name=_("Precision"))
    latest_active_BC = models.BooleanField(default=False,
                                           verbose_name=_("Is B.C. date"))
    gender = models.CharField(max_length=2,
                              choices=constants.GENDER_CHOICES,
                              default=u'N', verbose_name=_("gender"))
    nationality = models.ForeignKey("Country", null=True, blank=True,
                                    verbose_name=_("nationality"))
    headquarter_city = models.ForeignKey(
        "City", null=True, blank=True,
        help_text=_("Office / headquarters \
                    location (for corporate \
                    creators only)"),
        verbose_name=_("office / headquarters"))
    related_creators = models.ManyToManyField(
        "self", through="RelatedCreator",
        symmetrical=False, null=True, blank=True,
        verbose_name=_("related creators"))
    biography = models.TextField(
        null=True, blank=True,
        verbose_name=_("biographical / historical note"))
    website = models.URLField(null=True, blank=True,
                              verbose_name=_("website"))
    photo = models.ForeignKey("DigitalObject", null=True, blank=True,
                              verbose_name=_("photo"))
    primary_publications = models.ManyToManyField(
        Publication,
        null=True, blank=True,
        related_name="primary_bibliography_for",
        verbose_name=_("primary bibliography"))
    secondary_publications = models.ManyToManyField(
        Publication,
        null=True, blank=True,
        related_name="secondary_bibliography_for",
        verbose_name=_("secondary bibliography"))
    awards_text = models.TextField(null=True, blank=True,
                                   verbose_name=_("awards (plain text)"))
    biblio_text = models.TextField(null=True, blank=True,
                                   verbose_name=_("bibliography (plain text)"))
    biblio_text_es = models.TextField(
        null=True, blank=True,
        verbose_name=_("bibliography (plain text, Spanish)"))
    secondary_biblio_text = models.TextField(
        null=True, blank=True,
        verbose_name=_("secondary bibliography (plain text)"))
    secondary_biblio_text_es = models.TextField(
        null=True, blank=True,
        verbose_name=_("secondary bibliography (plain text, Spanish)"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True,
                                 verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True,
                                        verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))
    profiler_name = models.CharField(max_length=255, null=True, blank=True,
                                     default='',
                                     verbose_name=_("profiler name"))
    profiler_entry_date = models.CharField(
        max_length=255,
        null=True, blank=True, default='',
        verbose_name=_("profile entry date"))
    tags = TaggableManager(verbose_name="Tags",
                           help_text="A comma-separated list of tags.",
                           blank=True)

    class Meta:
        ordering = ['creator_name']

    def birth_date_display(self):
        return display_date(self.birth_date,
                            self.birth_date_precision,
                            self.birth_date_BC)
    birth_date_display.short_description = _("Birth date")

    def death_date_display(self):
        return display_date(self.death_date,
                            self.death_date_precision,
                            self.death_date_BC)
    death_date_display.short_description = _("Death date")

    def earliest_active_display(self):
        return display_date(self.earliest_active,
                            self.earliest_active_precision,
                            self.earliest_active_BC)
    earliest_active_display.short_description = _("Earliest active")

    def latest_active_display(self):
        return display_date(self.latest_active,
                            self.latest_active_precision,
                            self.latest_active_BC)
    latest_active_display.short_description = _("Latest active")

    def display_name_lastfirst(self):
        if self.creator_type == u'corp':
            name = self.org_name
        elif self.creator_type == u'family':
            name = "The " + self.family_name + " Family"
        else:
            name = ''
            if self.family_name:
                name += self.family_name
                if self.suffix:
                    name += ' ' + self.suffix + ', '
                else:
                    name += ', '
            if self.prefix:
                name += self.prefix + ' '
            if self.given_name:
                name += self.given_name + ' '
            if self.middle_name:
                name += self.middle_name + ' '
            name = name.rstrip(', ')
        return name

    def display_name(self):
        if self.creator_type == u'corp':
            name = self.org_name
        elif self.creator_type == u'family':
            name = "The " + self.family_name + " Family"
        else:
            name = ''
            if self.prefix:
                name += self.prefix + ' '
            if self.given_name:
                name += self.given_name + ' '
            if self.middle_name:
                name += self.middle_name + ' '
            if self.family_name:
                name += self.family_name + ' '
            if self.suffix:
                name += self.suffix
            name = name.rstrip()
        return name

    def has_system_links(self):
        if RelatedCreator.objects.filter(first_creator=self).exists():
            return True
        if RelatedCreator.objects.filter(second_creator=self).exists():
            return True
        if WorkRecordCreator.objects.filter(creator=self).exists():
            return True
        if Production.objects.filter(theater_companies=self).exists():
            return True
        if DirectingMember.objects.filter(person=self).exists():
            return True
        if CastMember.objects.filter(person=self).exists():
            return True
        if DesignMember.objects.filter(person=self).exists():
            return True
        if TechMember.objects.filter(person=self).exists():
            return True
        if ProductionMember.objects.filter(person=self).exists():
            return True
        if DocumentationMember.objects.filter(person=self).exists():
            return True
        if AdvisoryMember.objects.filter(person=self).exists():
            return True
        if FestivalParticipant.objects.filter(participant=self).exists():
            return True
        if DigitalObject.objects.filter(object_creator=self).exists():
            return True
        if DigitalObject.objects.filter(related_creator=self).exists():
            return True
        if AwardCandidate.objects.filter(recipient=self).exists():
            return True
        if Production.objects.filter(related_organizations=self).exists():
            return True
        return False

    def system_links(self):
        works = ''
        if RelatedCreator.objects.filter(first_creator=self).exists():
            for obj in RelatedCreator.objects.filter(first_creator=self):
                works += "RelatedCreator: " + str(obj.pk) + "\n"
        if RelatedCreator.objects.filter(second_creator=self).exists():
            for obj in RelatedCreator.objects.filter(second_creator=self):
                works += "RelatedCreator: " + str(obj.pk) + "\n"
        if WorkRecordCreator.objects.filter(creator=self).exists():
            for obj in WorkRecordCreator.objects.filter(creator=self):
                works += "WorkRecordCreator: " + str(obj.pk) + "\n"
        if Production.objects.filter(theater_companies=self).exists():
            for obj in Production.objects.filter(theater_companies=self):
                works += "Production: " + str(obj.pk) + "\n"
        if Production.objects.filter(related_organizations=self).exists():
            for obj in Production.objects.filter(related_organizations=self):
                works += "Production: " + str(obj.pk) + "\n"
        if DirectingMember.objects.filter(person=self).exists():
            for obj in DirectingMember.objects.filter(person=self):
                works += "DirectingMember: " + str(obj.pk) + "\n"
        if CastMember.objects.filter(person=self).exists():
            for obj in CastMember.objects.filter(person=self):
                works += "CastMember: " + str(obj.pk) + "\n"
        if DesignMember.objects.filter(person=self).exists():
            for obj in DesignMember.objects.filter(person=self):
                works += "DesignMember: " + str(obj.pk) + "\n"
        if TechMember.objects.filter(person=self).exists():
            for obj in TechMember.objects.filter(person=self):
                works += "TechMember: " + str(obj.pk) + "\n"
        if ProductionMember.objects.filter(person=self).exists():
            for obj in ProductionMember.objects.filter(person=self):
                works += "ProductionMember: " + str(obj.pk) + "\n"
        if DocumentationMember.objects.filter(person=self).exists():
            for obj in DocumentationMember.objects.filter(person=self):
                works += "DocumentationMember: " + str(obj.pk) + "\n"
        if AdvisoryMember.objects.filter(person=self).exists():
            for obj in AdvisoryMember.objects.filter(person=self):
                works += "AdvisoryMember: " + str(obj.pk) + "\n"
        if FestivalParticipant.objects.filter(participant=self).exists():
            for obj in FestivalParticipant.objects.filter(participant=self):
                works += "FestivalParticipant: " + str(obj.pk) + "\n"
        if DigitalObject.objects.filter(object_creator=self).exists():
            for obj in DigitalObject.objects.filter(object_creator=self):
                works += "DigitalObject: " + str(obj.pk) + "\n"
        if DigitalObject.objects.filter(related_creator=self).exists():
            for obj in DigitalObject.objects.filter(related_creator=self):
                works += "DigitalObject: " + str(obj.pk) + "\n"
        if AwardCandidate.objects.filter(recipient=self).exists():
            for obj in AwardCandidate.objects.filter(recipient=self):
                works += "AwardCandidate: " + str(obj.pk) + "\n"
        if works == "":
            return False
        else:
            return works

    def has_works(self):
        if WorkRecordCreator.objects.filter(
            creator=self, work_record__published=True).exists():
            return True
        else:
            return False

    def works(self):
        records = []
        wrc = WorkRecordCreator.objects.filter(creator=self,
                                               work_record__published=True)
        for record in wrc:
            if record.work_record.creation_date:
                date = record.work_record.creation_date_display()
            else:
                date = ""
            x = {'record_id': record.work_record.pk,
                 'record_title': record.work_record.title,
                 'function': record.function.title, 'date': date}
            records.append(x)
        return records

    def has_productions(self):
        result = False
        if self.directing_team_for.filter(published=True).count() > 0:
            result = True
        elif self.cast_member_for.filter(published=True).count() > 0:
            result = True
        elif self.design_team_for.filter(published=True).count() > 0:
            result = True
        elif self.technical_team_for.filter(published=True).count() > 0:
            result = True
        elif self.production_team_for.filter(published=True).count() > 0:
            result = True
        elif self.documentation_team_for.filter(published=True).count() > 0:
            result = True
        elif self.advisory_team_for.filter(published=True).count() > 0:
            result = True
        elif self.company_productions.filter(published=True).count() > 0:
            result = True
        elif self.productions_related_to.filter(published=True).count() > 0:
            result = True
        return result

    def productions(self):
        prods = []
        if self.directing_team_for.exists():
            for dt in self.directing_team_for.filter(
                published=True).distinct().order_by('-begin_date'):
                dms = DirectingMember.objects.filter(
                    person=self, production=dt,
                    production__published=True)
                roles = []
                for dm in dms:
                    roles.append(dm.function.title)
                x = {'prod_id': dt.pk,
                     'prod_title': dt.title,
                     'venue': dt.venue,
                     'date_range': dt.display_date_range(),
                     'role': ', '.join(roles)}
                prods.append(x)
        if self.cast_member_for.exists():
            for cm in self.cast_member_for.filter(
                published=True).distinct().order_by('-begin_date'):
                cms = CastMember.objects.filter(person=self,
                                                production=cm
                                                , production__published=True)
                roles = []
                for member in cms:
                    if member.function.title == "Actor / actress" \
                    and member.role:
                        roles.append(member.role.title)
                    else:
                        roles.append(member.function.title)
                x = {'prod_id': cm.pk,
                     'prod_title': cm.title,
                     'venue': cm.venue,
                     'date_range': cm.display_date_range(),
                     'role': ', '.join(roles)}
                prods.append(x)
        if self.design_team_for.exists():
          for dt in self.design_team_for.filter(
            published=True).distinct().order_by('-begin_date'):
                dms = DesignMember.objects.filter(person=self,
                                                  production=dt,
                                                  production__published=True)
                roles = []
                for dm in dms:
                    for role in dm.functions.all():
                        roles.append(role.title)
                x = {'prod_id': dt.pk,
                     'prod_title': dt.title,
                     'venue': dt.venue,
                     'date_range': dt.display_date_range(),
                     'role': ', '.join(roles)}
                prods.append(x)
        if self.technical_team_for.exists():
            for dt in self.technical_team_for.filter(
                published=True).distinct().order_by('-begin_date'):
                tms = TechMember.objects.filter(person=self,
                                                production=dt,
                                                production__published=True)
                roles = []
                for tm in tms:
                    roles.append(tm.function.title)
                x = {'prod_id': dt.pk,
                     'prod_title': dt.title,
                     'venue': dt.venue,
                     'date_range': dt.display_date_range(),
                     'role': ', '.join(roles)}
                prods.append(x)
        if self.production_team_for.exists():
            for dt in self.production_team_for.filter(
                published=True).distinct().order_by('-begin_date'):
                pms = ProductionMember.objects.filter(person=self,
                                                      production=dt,
                                                      production__published=True)
                roles = []
                for pm in pms:
                    roles.append(pm.function.title)
                x = {'prod_id': dt.pk,
                     'prod_title': dt.title,
                     'venue': dt.venue,
                     'date_range': dt.display_date_range(),
                     'role': ', '.join(roles)}
                prods.append(x)
        if self.documentation_team_for.exists():
            for dt in self.documentation_team_for.filter(
                published=True).distinct().order_by('-begin_date'):
                dms = DocumentationMember.objects.filter(person=self,
                                                         production=dt,
                                                         production__published=True)
                roles = []
                for dm in dms:
                    roles.append(dm.function.title)
                x = {'prod_id': dt.pk,
                     'prod_title': dt.title,
                     'venue': dt.venue,
                     'date_range': dt.display_date_range(),
                     'role': ', '.join(roles)}
                prods.append(x)
        if self.advisory_team_for.exists():
            for dt in self.advisory_team_for.filter(
                published=True).distinct().order_by('-begin_date'):
                ams = AdvisoryMember.objects.filter(person=self,
                                                    production=dt,
                                                    production__published=True)
                roles = []
                for am in ams:
                    roles.append(am.function.title)
                x = {'prod_id': dt.pk,
                     'prod_title': dt.title,
                     'venue': dt.venue,
                     'date_range': dt.display_date_range(),
                     'role': ', '.join(roles)}
                prods.append(x)
        if self.company_productions.exists():
            for dt in self.company_productions.filter(
                published=True).distinct().order_by('-begin_date'):
                x = {'prod_id': dt.pk,
                     'prod_title': dt.title,
                     'venue': dt.venue,
                     'date_range': dt.display_date_range(),
                     'role': 'Theater company' }
                prods.append(x)
        if self.productions_related_to.exists():
            for dt in self.productions_related_to.filter(
                published=True).distinct().order_by('-begin_date'):
                x = {'prod_id': dt.pk,
                     'prod_title': dt.title,
                     'venue': dt.venue,
                     'date_range': dt.display_date_range(),
                     'role': 'Related organization'}
                prods.append(x)
        return prods
        
    def display_roles(self):
        roles = []
        rolestring = ""

        dm = DirectingMember.objects.filter(person=self)
        if dm:
            for time in dm:
                roles.append(time.function.title)
        if CastMember.objects.filter(person=self):
            if self.gender == 'f':
                roles.append('actress')
            else:
                roles.append('actor')
        dm = DesignMember.objects.filter(person=self)
        if dm:
            for member in dm:
                for role in member.functions.all():
                    roles.append(role.title)
        pm = ProductionMember.objects.filter(person=self)
        if pm:
            for time in pm:
                roles.append(time.function.title)
        tm = TechMember.objects.filter(person=self)
        if tm:
            for time in tm:
                roles.append(time.function.title)
        dm = DocumentationMember.objects.filter(person=self)
        if dm:
            for time in dm:
                roles.append(time.function.title)
        am = AdvisoryMember.objects.filter(person=self)
        if am:
            for time in am:
                roles.append(time.function.title)
        wrc = WorkRecordCreator.objects.filter(creator=self)
        if wrc:
            for time in wrc:
                roles.append(time.function.title)

        # now put them in a list
        roles = make_unique(roles)
        rolestring = ', '.join(roles)
        rolestring = rolestring.capitalize()
        
        return rolestring
    display_roles.short_description = _("Roles")
    
    def has_related_creators(self):
        if self.first_creator_to.exists(): 
            return True
        else:
            return False
        
    def related_creators_relationship(self):
        return RelatedCreator.objects.filter(
            first_creator=self).order_by('function__ordinal')
    
    def creator_relationship(self):
        relationship = []
        relatedCreator_qs = RelatedCreator.objects.filter(first_creator=self)
        for relatedCreator in relatedCreator_qs:
            a_dict = {
                'Relationship': relatedCreator.get_relationship_display,
                'CreatorName': relatedCreator.second_creator.display_name,
                'Function': relatedCreator.function,
                'Since': relatedCreator.relationship_since_display,
                'Until': relatedCreator.relationship_until_display}
            relationship.append(a_dict)
        return relationship

    
    """    
    def same_birthplace_creators(self):
        if not self.birth_location:
            return False
        else:
            bp = self.birth_location
            rc = Creator.objects.filter(birth_location=bp).filter(published=True)
            rel = 'location'
        if not rc:
            bc = bp.city
            rc = Creator.objects.filter(birth_location__city=bc).filter(published=True)
            rel = 'city'
        
        x = {'rc': rc, 'rel': rel}
        return x
    """
    
    def same_production_creators(self):
        if not self.has_productions():
            return False
        else:
            productions = self.productions()
            # Pick one at random
            p = choice(productions)['prod_id']
            p = Production.objects.get(id=p)
            people = p.all_production_creators()
            # Remove yourself from the list
            for x in people:
              if x['person'] == self:
                people.remove(x)
            # Shuffle it up
            shuffle(people)
            people = people[:3]
        
            return { 'title': p.title, 'creators': people }

    def has_digital_objects(self):
        if DigitalObject.objects.filter(
            related_creator=self,
            digi_object_format=DigitalObjectType.objects.get(
                title="Image")).exists():
            return True
        else:
            return False

    def has_images(self):
        if DigitalObject.objects.filter(
            related_creator=self,
            digi_object_format=DigitalObjectType.objects.get(
                title="Image")).exists():
            return True
        else:
            return False

    def has_videos(self):
        if DigitalObject.objects.filter(
            related_creator=self,
            digi_object_format=DigitalObjectType.objects.get(
                title="Video recording"), ready_to_stream=True).exists():
            return True
        else:
            return False

    def has_audio(self):
        if DigitalObject.objects.filter(
            related_creator=self,
            digi_object_format=DigitalObjectType.objects.get(
                title="Audio recording")).exists():
            return True
        else:
            return False

    def __unicode__(self):
        if self.birth_date and self.death_date:
            return "%s, %s-%s (%s)" % (self.creator_name,
                                       self.birth_date_display(),
                                       self.death_date_display(), self.pk)
        if self.birth_date:
            return "%s, %s- (%s)" % (self.creator_name,
                                     self.birth_date_display(),
                                     self.pk)
        else:
            return "%s (%s)" % (self.creator_name, self.pk)

def update_creator_name(sender, **kwargs):
    obj = kwargs['instance']
    obj.creator_name = obj.display_name_lastfirst()
    obj.creator_ascii_name = unidecode(obj.creator_name)
    obj.creator_display_name = obj.display_name()
    obj.creator_display_ascii_name = unidecode(obj.creator_display_name)

pre_save.connect(update_creator_name, sender=Creator)

class RelatedCreator(models.Model):
    """Information about relationships between creators - members of organizations, family members, etc.
    """
    first_creator = models.ForeignKey(Creator, related_name="first_creator_to", verbose_name=_("creator 1"))
    relationship = models.CharField(max_length=12, choices=constants.CREATOR_RELATIONSHIP_TYPES, verbose_name=_("relationship"))
    second_creator = models.ForeignKey(Creator, related_name="second_creator_to", verbose_name=_("related creator"))
    function = models.ForeignKey("OrgFunction", null=True, blank=True, help_text=_("If the relationship is membership in an organization, select the member's function in the organization here."), verbose_name=_("function"))
    relationship_since = models.DateField(null=True, blank=True, help_text=_("Click 'Today' to see today's date in the proper date format."), verbose_name=_("relationship since"))
    relationship_since_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'y', null=True, blank=True, verbose_name=_("precision"))
    relationship_since_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    relationship_until = models.DateField(null=True, blank=True, help_text=_("Click 'Today' to see today's date in the proper date format."), verbose_name=_("relationship until"))
    relationship_until_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'y', null=True, blank=True, verbose_name=_("precision"))
    relationship_until_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    
    def relationship_since_display(self):
        return display_date(self.relationship_since, self.relationship_since_precision, self.relationship_since_BC)
    relationship_since_display.short_description = _("Relationship since")
    
    def relationship_until_display(self):
        return display_date(self.relationship_until, self.relationship_until_precision, self.relationship_until_BC)
    relationship_until_display.short_description = _("Relationship until")
    
    def __unicode__(self):
        return "%s %s %s" % (self.first_creator.display_name(), self.get_relationship_display(), self.second_creator.display_name())

class Location(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    title_ascii = models.CharField(max_length=255, verbose_name=_("title (ASCII)"))
    title_variants = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("title variants"))
    is_venue = models.BooleanField(default=False, verbose_name=_("Is a venue"), help_text=_("Check this box if productions / festivals occur at this location"))
    venue_type = models.ForeignKey("VenueType", null=True, blank=True, verbose_name=_("venue type"))
    begin_date = models.DateField(null=True, blank=True, help_text=_("Click 'Today' to see today's date in the proper date format."), verbose_name=_(u"begin date"))
    begin_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'y', null=True, blank=True, verbose_name=_(u"precision"))
    begin_date_BC = models.BooleanField(default=False, verbose_name=_(u"Is B.C. date"))
    end_date = models.DateField(null=True, blank=True, help_text=_("Click 'Today' to see today's date in the proper date format."), verbose_name=_(u"end date"))
    end_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'y', null=True, blank=True, verbose_name=_(u"precision"))
    end_date_BC = models.BooleanField(default=False, verbose_name=_(u"Is B.C. date"))
    address = models.CharField(max_length=100, verbose_name=_("street address"), null=True, blank=True)
    address2 = models.CharField(max_length=100, verbose_name=_("street address (line 2)"), null=True, blank=True)
    city = models.ForeignKey("City", null=True, blank=True, verbose_name=_("city"))
#    state = models.CharField(max_length=100, verbose_name=_("state/province"), null=True, blank=True)
    postal_code = models.CharField(max_length=20, verbose_name=_("postal code"), null=True, blank=True)
    country = models.ForeignKey("Country", verbose_name=_("country"))
    lat = models.CharField(max_length=20, verbose_name=_("latitude"), null=True, blank=True)
    lon = models.CharField(max_length=20, verbose_name=_("longitude"), null=True, blank=True)
    altitude = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("altitude"))
    summary = models.TextField(null=True, blank=True, verbose_name=_("summary"))
    website = models.URLField(null=True, blank=True, verbose_name=_("website"))
    photo = models.ForeignKey("DigitalObject", related_name="locations", null=True, blank=True, verbose_name=_("photo"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))
    profiler_name = models.CharField(max_length=255, null=True, blank=True, default='', verbose_name=_("profiler name"))
    profiler_entry_date = models.CharField(max_length=255, null=True, blank=True, default='', verbose_name=_("profile entry date"))
    tags = TaggableManager(verbose_name="Tags", help_text="A comma-separated list of tags.", blank=True)

    def begin_date_display(self):
        return display_date(self.begin_date, self.begin_date_precision, self.begin_date_BC)
    begin_date_display.short_description = _("Begin date")
    
    def end_date_display(self):
        return display_date(self.end_date, self.end_date_precision, self.end_date_BC)
    end_date_display.short_description = _("End date")

    def __unicode__(self):
        if self.pk == 45:
            return ugettext(u"Unknown")
        if self.begin_date or self.end_date:
            return "%s (%s), %s-%s (%d)" % (self.title, self.country.name, self.begin_date_display(), self.end_date_display(), self.pk)
        else:
            return "%s (%s) (%d)" % (self.title, self.country.name, self.pk)

    def display_name(self):
        if self.pk == 45:
            return ugettext(u"Unknown")
        if self.begin_date or self.end_date:
            return "%s (%s), %s-%s" % (self.title, self.country.name, self.begin_date_display(), self.end_date_display())
        else:
            return "%s (%s)" % (self.title, self.country.name)

    def has_system_links(self):
        if Stage.objects.filter(venue=self).exists():
            return True
        if Production.objects.filter(venue=self).exists():
            return True
        if FestivalOccurrence.objects.filter(venue=self).exists():
            return True
        if Repository.objects.filter(location=self).exists():
            return True
        if DigitalObject.objects.filter(phys_obj_city=self).exists():
            return True
        if DigitalObject.objects.filter(related_venue=self).exists():
            return True
        return False
    
    def published_productions(self):
        return self.productions.filter(published=True).order_by('-begin_date')
    
    def has_images(self):
        if DigitalObject.objects.filter(related_venue=self, digi_object_format=DigitalObjectType.objects.get(title="Image")).exists():
            return True
        else:
            return False

    def has_videos(self):
        if DigitalObject.objects.filter(related_venue=self, digi_object_format=DigitalObjectType.objects.get(title="Video recording"), ready_to_stream=True).exists():
            return True
        else:
            return False

    def has_audio(self):
        if DigitalObject.objects.filter(related_venue=self, digi_object_format=DigitalObjectType.objects.get(title="Audio recording")).exists():
            return True
        else:
            return False

def update_location_name(sender, **kwargs):
    obj = kwargs['instance']
    obj.title_ascii = unidecode(obj.title)

pre_save.connect(update_location_name, sender=Location)

class Stage(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    title_variants = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("title variants"))
    venue = models.ForeignKey(Location, related_name="stages", verbose_name=_("venue"))
    square_footage = models.PositiveIntegerField(null=True, blank=True, help_text=_("Number only, no commas"), verbose_name=_("square footage"))
    stage_type = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("stage type"))
    stage_width = models.PositiveIntegerField(null=True, blank=True, help_text=_("Width of the stage, in feet"), verbose_name=_("stage width"))
    stage_depth = models.PositiveIntegerField(null=True, blank=True, help_text=_("Depth of the stage, in feet"), verbose_name=_("stage depth"))
    stage_height = models.PositiveIntegerField(null=True, blank=True, help_text=_("Amount of vertical space on stage, in feet"), verbose_name=_("stage height"))
    stage_lighting = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("stage lighting"))
    stage_sound = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("stage sound"))
    seating = models.PositiveIntegerField(null=True, blank=True, help_text=_("Number of audience members that can be accommodated"), verbose_name=_("seating"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    tags = TaggableManager(verbose_name="Tags", help_text="A comma-separated list of tags.", blank=True)
    
    def __unicode__(self):
        return "%s" % (self.title)
    
class WorkRecord(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    subtitle = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("subtitle"))
    title_variants = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("title variants"))
    ascii_title = models.CharField(max_length=255, verbose_name=_("ASCII title"))
    creators = models.ManyToManyField(Creator, through="WorkRecordCreator", verbose_name=_("creators"))
    creators_display = models.CharField(max_length=255, verbose_name=_("creators"))
    work_type = models.ForeignKey("WorkRecordType", verbose_name=_("work type"))
    subject = models.ManyToManyField(SubjectHeading, null=True, blank=True, related_name="works", verbose_name=_("subject"))
    genre = models.ForeignKey("WorkGenre", null=True, blank=True, help_text=_("The work's genre - e.g. drama, comedy"), verbose_name=_("genre"))
    culture = models.ForeignKey("WorkCulture", null=True, blank=True, help_text=_("The culture the work is a part of"), verbose_name=_("culture"))
    style = models.ForeignKey("WorkStyle", null=True, blank=True, help_text=_("A movement or period the work belongs to"), verbose_name=_("style"))
    lang = models.ManyToManyField("Language", null=True, blank=True, verbose_name=_("language"))
    creation_date = models.DateField(null=True, blank=True, help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("creation date"))
    creation_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'y', null=True, blank=True, verbose_name=_("Precision"))
    creation_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    publication_date = models.DateField(null=True, blank=True, help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("publication date"))
    publication_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'y', null=True, blank=True, verbose_name=_("Precision"))
    publication_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    publication_rights = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("publication rights"))
    performance_rights = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("performance rights"))
    website = models.URLField(null=True, blank=True, help_text=_("A site where users can find the text of this work"), verbose_name=_("website"))
    digital_copy = models.ForeignKey("DigitalObject", null=True, blank=True, verbose_name=_("digital copy"))
    summary = models.TextField(null=True, blank=True, verbose_name=_("summary"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    related_works = models.ManyToManyField("self", through="RelatedWork", symmetrical=False, null=True, blank=True, related_name="related_to", verbose_name=_("related works"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))
    awards_text = models.TextField(null=True, blank=True, verbose_name=_("awards (plain text)"))
    biblio_text = models.TextField(null=True, blank=True, verbose_name=_("bibliography (plain text)"))
    biblio_text_es = models.TextField(null=True, blank=True, verbose_name=_("bibliography (plain text, Spanish)"))
    secondary_biblio_text = models.TextField(null=True, blank=True, verbose_name=_("secondary bibliography (plain text)"))
    secondary_biblio_text_es = models.TextField(null=True, blank=True, verbose_name=_("secondary bibliography (plain text, Spanish)"))
    primary_publications = models.ManyToManyField(Publication, null=True, blank=True, related_name="workedrecord_primary_bibliography_for", verbose_name=_("primary bibliography"))
    secondary_publications = models.ManyToManyField(Publication, null=True, blank=True, related_name="workedrecord_secondary_bibliography_for", verbose_name=_("secondary bibliography"))
    profiler_name = models.CharField(max_length=255, null=True, blank=True, default='', verbose_name=_("profiler name"))
    profiler_entry_date = models.CharField(max_length=255, null=True, blank=True, default='', verbose_name=_("profile entry date"))
    tags = TaggableManager(verbose_name="Tags", help_text="A comma-separated list of tags.", blank=True)
    
    class Meta:
        ordering = ['title']

    def creation_date_display(self):
        return display_date(self.creation_date, self.creation_date_precision, self.creation_date_BC)
    creation_date_display.short_description = _("Creation date")
    
    def publication_date_display(self):
        return display_date(self.publication_date, self.publication_date_precision, self.publication_date_BC)
    publication_date_display.short_description = _("Publication date")

    def creators_display_links(self):
        cs = ""
        for wrc in WorkRecordCreator.objects.filter(work_record=self):
            cs += "<h4>" + wrc.function.title + ":</h4>"
            cs += "<a href='/creator/" + str(wrc.creator.id) + "'>"
            cs += wrc.creator.display_name()
            cs += "</a>, "
        cs = cs.rstrip(', ')
        return cs

    def language_display(self):
        language_qs = self.lang.all()
        langs = ""
        for language in language_qs:
            langs += language.name
            langs += ","
        langs = langs.rstrip(',')
        return langs
    
    def has_system_links(self):
        if AwardCandidate.objects.filter(work_record=self).exists():
            return True
        elif RelatedWork.objects.filter(first_work=self).exists():
            return True
        elif RelatedWork.objects.filter(second_work=self).exists():
            return True
        elif WorkRecordCreator.objects.filter(work_record=self).exists():
            return True
        elif Role.objects.filter(source_text=self).exists():
            return True
        elif Production.objects.filter(source_work=self).exists():
            return True
        elif DigitalObject.objects.filter(related_work=self).exists():
            return True
#        elif BibliographicRecord.objects.filter(work_record=self).exists():
#            return True
        else:
            return False

    def has_images(self):
        if DigitalObject.objects.filter(related_work=self, digi_object_format=DigitalObjectType.objects.get(title="Image")).exists():
            return True
        else:
            return False

    def has_videos(self):
        if DigitalObject.objects.filter(related_work=self, digi_object_format=DigitalObjectType.objects.get(title="Video recording"), ready_to_stream=True).exists():
            return True
        else:
            return False

    def has_audio(self):
        if DigitalObject.objects.filter(related_work=self, digi_object_format=DigitalObjectType.objects.get(title="Audio recording")).exists():
            return True
        else:
            return False

    def published_performances(self):
        return self.performances.filter(published=True)

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.work_type.name)

def update_wr_title(sender, **kwargs):
    obj = kwargs['instance']
    obj.ascii_title = unidecode(obj.title)

pre_save.connect(update_wr_title, sender=WorkRecord)

def update_workrecord_creators(sender, **kwargs):
    record = kwargs['instance'].work_record
    textstring = ''
    for c in WorkRecordCreator.objects.filter(work_record=record):
        textstring += c.creator.creator_name + ", "
    textstring = textstring.rstrip(', ')
    textstring = textstring[:255] if len(textstring) > 255 else textstring
    record.creators_display = textstring
    record.save()

class RelatedWork(models.Model):
    first_work = models.ForeignKey(WorkRecord, related_name="first_work_to", verbose_name=_("work"))
    relationship = models.CharField(max_length=5, choices=constants.RELATIONSHIP_TYPE_CHOICES, verbose_name=_("relationship"))
    second_work = models.ForeignKey(WorkRecord, related_name="second_work_to", verbose_name=_("related work"))
    
    def __unicode__(self):
        return "%s %s %s" % (self.first_work.title, self.get_relationship_display(), self.second_work.title)

class WorkRecordCreator(models.Model):
    creator = models.ForeignKey(Creator, verbose_name=_("creator"))
    work_record = models.ForeignKey(WorkRecord, verbose_name=_("work record"))
    function = models.ForeignKey("WorkRecordFunction", verbose_name=_("function"))
    
    def __unicode__(self):
        return self.creator.creator_name

post_save.connect(update_workrecord_creators, sender=WorkRecordCreator)

class Role(models.Model):
    source_text = models.ForeignKey(WorkRecord, related_name="roles", verbose_name=_("source text"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    
    def __unicode__(self):
        return "%s (%s)" % (self.title, self.source_text.title)

class WorkGenre(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    
    def __unicode__(self):
        return self.title

class WorkCulture(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    
    def __unicode__(self):
        return self.title

class WorkStyle(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    
    def __unicode__(self):
        return self.title
    
class Production(models.Model):
    source_work = models.ManyToManyField(WorkRecord, related_name="performances", verbose_name=_("source work"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    subtitle = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("subtitle"))
    ascii_title = models.CharField(max_length=255, verbose_name=_("ASCII title"))
    title_variants = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("title variants"))
    venue = models.ForeignKey(Location, related_name="productions", verbose_name=_("venue"))
    #stage = ChainedForeignKey(Stage, chained_field="venue", chained_model_field="venue", show_all=True, auto_choose=False, null=True, blank=True, verbose_name=_("stage"))
    stage = models.ForeignKey(Stage, null=True, blank=True, verbose_name=_("stage"))
    begin_date = models.DateField(null=True, blank=True, help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("begin date"))
    begin_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'f', verbose_name=_("Precision"))
    begin_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    end_date = models.DateField(null=True, blank=True, help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("end date"))
    end_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'f', verbose_name=_("Precision"))
    end_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    num_performances = models.IntegerField(null=True, blank=True, verbose_name=_("Number of performances"))
    is_special_performance = models.BooleanField(default=False, verbose_name=_("Special performance?"))
#    special_performance_type = models.CharField(max_length=12, choices=constants.SPECIAL_PERFORMANCE_CHOICES, null=True, blank=True, verbose_name=_("Type"))
    special_performance_type = models.ForeignKey(SpecialPerformanceType, related_name="special_performance_type", default=None, null=True, blank=True, verbose_name=_("Type"))
#    special_performance_type_tmp = models.ForeignKey(SpecialPerformanceType, related_name="special_performance_type_tmp", default=None, null=True, blank=True, verbose_name=_("Type"))
    directing_team = models.ManyToManyField(Creator, through="DirectingMember", null=True, blank=True, related_name="directing_team_for", verbose_name=_("directing team"))
    cast = models.ManyToManyField(Creator, through="CastMember", related_name="cast_member_for", verbose_name=_("cast"))
    design_team = models.ManyToManyField(Creator, through="DesignMember", null=True, blank=True, related_name="design_team_for", verbose_name=_("design team"))
    technical_team = models.ManyToManyField(Creator, through="TechMember", null=True, blank=True, related_name="technical_team_for", verbose_name=_("technical team"))
    production_team = models.ManyToManyField(Creator, through="ProductionMember", null=True, blank=True, related_name="production_team_for", verbose_name=_("production team"))
    documentation_team = models.ManyToManyField(Creator, through="DocumentationMember", null=True, blank=True, related_name="documentation_team_for", verbose_name=_("documentation team"))
    advisory_team = models.ManyToManyField(Creator, through="AdvisoryMember", null=True, blank=True, related_name="advisory_team_for", verbose_name=_("advisory team"))
    related_organizations = models.ManyToManyField(Creator, null=True, blank=True, related_name="productions_related_to", verbose_name=_("related organizations"))
    premier = models.CharField(max_length=2, choices=constants.PREMIER_CHOICES, null=True, blank=True, verbose_name=_("premiere"))
    website = models.URLField(null=True, blank=True, verbose_name=_("website"))
    primary_publications = models.ManyToManyField(Publication, null=True, blank=True, related_name="production_primary_bibliography_for", verbose_name=_("primary bibliography"))
    secondary_publications = models.ManyToManyField(Publication, null=True, blank=True, related_name="production_secondary_bibliography_for", verbose_name=_("secondary bibliography"))
    awards_text = models.TextField(null=True, blank=True, verbose_name=_("awards (plain text)"))
    biblio_text = models.TextField(null=True, blank=True, verbose_name=_("bibliography (plain text)"))
    biblio_text_es = models.TextField(null=True, blank=True, verbose_name=_("bibliography (plain text, Spanish)"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))
    theater_companies = models.ManyToManyField(Creator, null=True, blank=True, related_name="company_productions")
    profiler_name = models.CharField(max_length=255, null=True, blank=True, default='', verbose_name=_("profiler name"))
    profiler_entry_date = models.CharField(max_length=255, null=True, blank=True, default='', verbose_name=_("profile entry date"))
    tags = TaggableManager(verbose_name="Tags", help_text="A comma-separated list of tags.", blank=True)

    class Meta:
        ordering = ['title']

    def begin_date_display(self):
        return display_date(self.begin_date, self.begin_date_precision, self.begin_date_BC)
    begin_date_display.short_description = _("Begin date")
    
    def end_date_display(self):
        return display_date(self.end_date, self.end_date_precision, self.end_date_BC)
    end_date_display.short_description = _("End date")

    def display_directors(self):
        ds = ""
        for person in self.directing_team.filter(directingmember__function=DirectingTeamFunction.objects.get(title='Director')):
            ds += person.display_name()
            ds += ", "
        ds = ds[:-2]
        return ds
    display_directors.short_description = _("Directors")

    def display_directors_links(self):
        ds = ""
        for person in self.directing_team.filter(directingmember__function=DirectingTeamFunction.objects.get(title='Director')):
            ds += "<a href='/creator/" + str(person.id) + "'>"
            ds += person.display_name()
            ds += "</a>, "
        ds = ds[:-2]
        return ds
    display_directors_links.short_description = _("Directors")

    def all_production_creators(self):
        """
        Return a list of all creators attached to this production (directors, cast, tech, etc.) with function
        Format: [{'person': i, 'function': x}, {'person': j, 'function': y}]
        """
        allpeople = []
        for p in DirectingMember.objects.filter(production=self).filter(production__published=True):
            allpeople.append({'person': p.person, 'function': p.function})
        for p in CastMember.objects.filter(production=self).filter(production__published=True):
            allpeople.append({'person': p.person, 'function': p.function})
        for p in DesignMember.objects.filter(production=self).filter(production__published=True):
            allpeople.append({'person': p.person, 'function': p.functions})
        for p in TechMember.objects.filter(production=self).filter(production__published=True):
            allpeople.append({'person': p.person, 'function': p.function})
        for p in ProductionMember.objects.filter(production=self).filter(production__published=True):
            allpeople.append({'person': p.person, 'function': p.function})
        for p in DocumentationMember.objects.filter(production=self).filter(production__published=True):
            allpeople.append({'person': p.person, 'function': p.function})
        for p in AdvisoryMember.objects.filter(production=self).filter(production__published=True):
            allpeople.append({'person': p.person, 'function': p.function})
        return allpeople

    def has_system_links(self):
        if DirectingMember.objects.filter(production=self).exists():
            return True
        elif CastMember.objects.filter(production=self).exists():
            return True
        elif DesignMember.objects.filter(production=self).exists():
            return True
        elif TechMember.objects.filter(production=self).exists():
            return True
        elif ProductionMember.objects.filter(production=self).exists():
            return True
        elif DocumentationMember.objects.filter(production=self).exists():
            return True
        elif AdvisoryMember.objects.filter(production=self).exists():
            return True
        elif AwardCandidate.objects.filter(production=self).exists():
            return True
        elif FestivalOccurrence.objects.filter(productions=self).exists():
            return True
        elif DigitalObject.objects.filter(related_production=self).exists():
            return True
        elif self.source_work.count():
            return True
        else:
            return False

    def all_directors(self):
        directors = []
        for person in self.directing_team.filter(published=True).distinct():
            x = {}
            x['person'] = person
            dms = DirectingMember.objects.filter(person=person, production=self)
            roles = []
            for dm in dms:
                roles.append(dm.function.title)
            x['functions'] = ', '.join(roles)
            directors.append(x)
        return directors

    def all_cast(self):
        cast = []
        for person in self.cast.filter(published=True).distinct():
            x = {}
            x['person'] = person
            cms = CastMember.objects.filter(person=person, production=self)
            roles = []
            for cm in cms:
                if cm.role:
                    roles.append(cm.role.title)
                else:
                    roles.append(cm.function.title)
            x['roles'] = '; '.join(roles)
            cast.append(x)
        return cast

    def all_designers(self):
        designers = []
        for person in self.design_team.filter(published=True).distinct():
            x = {}
            x['person'] = person
            dms = DesignMember.objects.filter(person=person, production=self)
            roles = []
            for dm in dms:
                for role in dm.functions.all():
                    roles.append(role.title)
            x['functions'] = ', '.join(roles)
            designers.append(x)
        return designers

    def all_techs(self):
        techs = []
        for person in self.technical_team.filter(published=True).distinct():
            x = {}
            x['person'] = person
            tms = TechMember.objects.filter(person=person, production=self)
            roles = []
            for tm in tms:
                roles.append(tm.function.title)
            x['functions'] = ', '.join(roles)
            techs.append(x)
        return techs

    def all_producers(self):
        producers = []
        for person in self.production_team.filter(published=True).distinct():
            x = {}
            x['person'] = person
            pms = ProductionMember.objects.filter(person=person, production=self)
            roles = []
            for pm in pms:
                roles.append(pm.function.title)
            x['functions'] = ', '.join(roles)
            producers.append(x)
        return producers

    def all_documentation(self):
        documentation = []
        for person in self.documentation_team.filter(published=True).distinct():
            x = {}
            x['person'] = person
            dms = DocumentationMember.objects.filter(person=person, production=self)
            roles = []
            for dm in dms:
                roles.append(dm.function.title)
            x['functions'] = ', '.join(roles)
            documentation.append(x)
        return documentation

    def all_advisors(self):
        advisors = []
        for person in self.advisory_team.filter(published=True).distinct():
            x = {}
            x['person'] = person
            ams = AdvisoryMember.objects.filter(person=person, production=self)
            roles = []
            for am in ams:
                roles.append(am.function.title)
            x['functions'] = ', '.join(roles)
            advisors.append(x)
        return advisors

    def display_date_range(self):
        if self.begin_date and self.end_date:
            if self.begin_date == self.end_date:
                return self.begin_date_display()
            else:
                return "%s - %s" % (self.begin_date_display(), self.end_date_display())
        elif self.begin_date:
            return self.begin_date_display()
        else:
            return ''
    
    def all_festival_occurrence(self):
        
        festival_occurrence = []
        festival_occurrence_qs = self.festivaloccurrence_set.filter(published=True)
        for festival in festival_occurrence_qs:
            a_dict = {}
            a_dict['festival_occurrence'] = festival
            festival_occurrence.append(a_dict)
            
        return festival_occurrence

    def has_images(self):
        if DigitalObject.objects.filter(related_production=self, digi_object_format=DigitalObjectType.objects.get(title="Image")).exists():
            return True
        else:
            return False

    def has_videos(self):
        if DigitalObject.objects.filter(related_production=self, digi_object_format=DigitalObjectType.objects.get(title="Video recording"), ready_to_stream=True).exists():
            return True
        else:
            return False

    def has_audio(self):
        if DigitalObject.objects.filter(related_production=self, digi_object_format=DigitalObjectType.objects.get(title="Audio recording")).exists():
            return True
        else:
            return False

    def __unicode__(self):
        if self.begin_date:
            return "%s (%s, %s)" % (self.title, self.venue.title, self.begin_date_display())
        else:
            return "%s (%s)" % (self.title, self.venue.title)

def update_prod_title(sender, **kwargs):
    obj = kwargs['instance']
    obj.ascii_title = unidecode(obj.title)

pre_save.connect(update_prod_title, sender=Production)

class DirectingMember(models.Model):
    person = models.ForeignKey(Creator, verbose_name=_("person"))
    production = models.ForeignKey(Production, verbose_name=_("production"))
    function = models.ForeignKey("DirectingTeamFunction", verbose_name=_("function"))

    def __unicode__(self):
        return "%s (%s), %s" % (self.person.creator_name, self.function.title, self.production)

class CastMember(models.Model):
    person = models.ForeignKey(Creator, verbose_name=_("person"))
    production = models.ForeignKey(Production, verbose_name=_("production"))
    function = models.ForeignKey("CastMemberFunction", verbose_name=_("function"))
    role = models.ForeignKey(Role, null=True, blank=True, default=None, verbose_name=_("role"))

    def __unicode__(self):
        return "%s (%s), %s" % (self.person.creator_name, self.function.title, self.production)

class DesignMember(models.Model):
    person = models.ForeignKey(Creator, verbose_name=_("person"))
    production = models.ForeignKey(Production, verbose_name=_("production"))
    functions = models.ManyToManyField("DesignTeamFunction", related_name="functions", verbose_name=_("function"))

    def __unicode__(self):
        return "%s (%s), %s" % (self.person.creator_name, '', self.production)

class TechMember(models.Model):
    person = models.ForeignKey(Creator, verbose_name=_("person"))
    production = models.ForeignKey(Production, verbose_name=_("production"))
    function = models.ForeignKey("TechTeamFunction", verbose_name=_("function"))

    def __unicode__(self):
        return "%s (%s), %s" % (self.person.creator_name, self.function.title, self.production)

class ProductionMember(models.Model):
    person = models.ForeignKey(Creator, verbose_name=_("person"))
    production = models.ForeignKey(Production, verbose_name=_("production"))
    function = models.ForeignKey("ProductionTeamFunction", verbose_name=_("function"))

    def __unicode__(self):
        return "%s (%s), %s" % (self.person.creator_name, self.function.title, self.production)

class DocumentationMember(models.Model):
    person = models.ForeignKey(Creator, verbose_name=_("person"))
    production = models.ForeignKey(Production, verbose_name=_("production"))
    function = models.ForeignKey("DocumentationTeamFunction", verbose_name=_("function"))

    def __unicode__(self):
        return "%s (%s), %s" % (self.person.creator_name, self.function.title, self.production)

class AdvisoryMember(models.Model):
    person = models.ForeignKey(Creator, verbose_name=_("person"))
    production = models.ForeignKey(Production, verbose_name=_("production"))
    function = models.ForeignKey("AdvisoryTeamFunction", verbose_name=_("function"))

    def __unicode__(self):
        return "%s (%s), %s" % (self.person.creator_name, self.function.title, self.production)

class Festival(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    
    def has_images(self):
        fo = FestivalOccurrence.objects.filter(festival_series=self)
        for obj in fo:
            if obj.has_images():
                return True
        
        return False

    def has_videos(self):
        fo = FestivalOccurrence.objects.filter(festival_series=self)
        for obj in fo:
            if obj.has_videos():
                return True
        
        return False

    def has_audio(self):
        fo = FestivalOccurrence.objects.filter(festival_series=self)
        for obj in fo:
            if obj.has_audio():
                return True
        
        return False

    def __unicode__(self):
        return self.title

class FestivalOccurrence(models.Model):
    
    festival_series = models.ForeignKey(Festival, verbose_name=_("festival series"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    ascii_title = models.CharField(max_length=255, verbose_name=_("ASCII title"))
    title_variants = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("title variants"))
 
    begin_date = models.DateField(help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("begin date"))
    begin_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'f', verbose_name=_("Precision"))
    begin_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    end_date = models.DateField(help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("end date"))
    end_date_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'f', verbose_name=_("Precision"))
    end_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    
    venue = models.ManyToManyField(Location, blank=True, default=None, verbose_name=_("venue"))
    participants = models.ManyToManyField(Creator, through="FestivalParticipant", null=True, blank=True, verbose_name=_("participants"))
    productions = models.ManyToManyField(Production, blank=True, default=None, verbose_name=_("productions"))
    primary_publications = models.ManyToManyField(Publication, null=True, blank=True, related_name="festival_primary_bibliography_for", verbose_name=_("primary bibliography"))
    
    awards_text = models.TextField(null=True, blank=True, verbose_name=_("awards"))
    program = models.TextField(null=True, blank=True, verbose_name=_("festival/conference program"))
    edu_program = models.TextField(null=True, blank=True, verbose_name=_("festival/conference educational program"))
    announcement = models.TextField(null=True, blank=True, verbose_name=_("festival/conference announcement"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    website = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("website"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))
    profiler_name = models.CharField(max_length=255, null=True, blank=True, default='', verbose_name=_("profiler name"))
    profiler_entry_date = models.CharField(max_length=255, null=True, blank=True, default='', verbose_name=_("profile entry date"))
    tags = TaggableManager(verbose_name="Tags", help_text="A comma-separated list of tags.", blank=True)

    def begin_date_display(self):
        return display_date(self.begin_date, self.begin_date_precision, self.begin_date_BC)
        
    def end_date_display(self):
        return display_date(self.end_date, self.end_date_precision, self.end_date_BC)

    def __unicode__(self):
        return "%s (%s - %s)" % (self.title, self.begin_date_display(), self.end_date_display())
    
    def has_images(self):
        if DigitalObject.objects.filter(related_festival=self, digi_object_format=DigitalObjectType.objects.get(title="Image")).exists():
            return True
        else:
            return False

    def has_videos(self):
        if DigitalObject.objects.filter(related_festival=self, digi_object_format=DigitalObjectType.objects.get(title="Video recording"), ready_to_stream=True).exists():
            return True
        else:
            return False

    def has_audio(self):
        if DigitalObject.objects.filter(related_festival=self, digi_object_format=DigitalObjectType.objects.get(title="Audio recording")).exists():
            return True
        else:
            return False

    def display_date_range(self):
        if self.begin_date and self.end_date:
            if self.begin_date == self.end_date:
                return self.begin_date_display()
            else:
                return "%s - %s" % (self.begin_date_display(), self.end_date_display())
        elif self.begin_date:
            return self.begin_date_display()
        else:
            return ''
        
    def all_participants(self):
        participants = []
        for person in self.participants.distinct():
            x = {}
            x['person'] = person
            fps = FestivalParticipant.objects.filter(participant=person, festival=self)
            roles = []
            for fp in fps:
                roles.append(fp.function.title)
            x['functions'] = ', '.join(roles)
            participants.append(x)
        return participants
    
    
def update_festival_occurrence_title(sender, **kwargs):
    obj = kwargs['instance']
    obj.ascii_title = unidecode(obj.title)

pre_save.connect(update_festival_occurrence_title, sender=FestivalOccurrence)


class FestivalParticipant(models.Model):
    participant = models.ForeignKey(Creator, verbose_name=_("participant"))
    festival = models.ForeignKey(FestivalOccurrence, verbose_name=_("festival"))
    function = models.ForeignKey("FestivalFunction", verbose_name=_("function"))
    
    def __unicode__(self):
        return "%s (%s), %s" % (self.participant.creator_name, self.function.title, self.festival)
    
class Repository(models.Model):
    repository_id = models.CharField(max_length=3, null=True, blank=True, verbose_name=_("repository ID"))
    title = models.CharField(max_length=200, verbose_name=_("title"))
    ascii_title = models.CharField(max_length=200, verbose_name=_("ASCII title"))
    location = models.ForeignKey(Location, verbose_name=_("location"))
    summary = models.TextField(null=True, blank=True, verbose_name=_("summary"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))
    
    class Meta:
        verbose_name_plural = "repositories"
    
    def __unicode__(self):
        return "Repository: %s" % (self.title,)

def update_repository_title(sender, **kwargs):
    obj = kwargs['instance']
    obj.ascii_title = unidecode(obj.title)

pre_save.connect(update_repository_title, sender=Repository)


class Collection(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    ascii_title = models.CharField(max_length=200, verbose_name=_("ASCII title"))
    repository = models.ForeignKey(Repository, related_name="collections", verbose_name=_("repository"))
    collection_id = models.CharField(max_length=4, verbose_name=_("collection ID"))
    url = models.URLField(null=True, blank=True, verbose_name=_("URL"))
#    summary = models.TextField(null=True, blank=True, verbose_name=_("summary"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))

    def has_viewable_objects(self):
        return DigitalObject.objects.filter(Q(published=True), Q(digi_object_format__title="Image", files__isnull=False) | Q(digi_object_format__title="Video recording", ready_to_stream=True)).filter(collection=self).exists()

    def __unicode__(self):
        return "Collection: %s" % (self.title,)

def update_collection_title(sender, **kwargs):
    obj = kwargs['instance']
    obj.ascii_title = unidecode(obj.title)

pre_save.connect(update_collection_title, sender=Collection)


def object_upload_path(instance, filename):
    extension = filename.split('.')[-1]
    rep_code = instance.digital_object.collection.repository.repository_id
    col_code = instance.digital_object.collection.collection_id
    obj_code = instance.digital_object.object_id
    seq_code = instance.seq_id
    
    new_filename = ''.join([rep_code, col_code, obj_code, seq_code, '001.', extension])

    if instance.digital_object.attention:
        instance.digital_object.attention += ''.join(['File: ', new_filename, 'Original filename: ', filename])
    else:
        instance.digital_object.attention = ''.join(['File: ', new_filename, 'Original filename: ', filename])

    return '/'.join(['digitalobjects', rep_code, col_code, new_filename])

def setup_new_object(sender, **kwargs):
    print 'in setup new object'
    instance = kwargs['instance']
    print instance
    if not instance.object_id:
        try:
            biggest_id = DigitalObject.objects.filter(collection=instance.collection).aggregate(Max('object_id'))
            biggest_id = '%06d' % (int(biggest_id['object_id__max']) + 1)
            instance.object_id = biggest_id
            print 'biggest id: ', biggest_id
        except:
            instance.object_id = '000001'

def setup_digital_file(sender, **kwargs):
    instance = kwargs['instance']
    if not instance.seq_id:
        try:
            biggest_id = DigitalFile.objects.filter(digital_object=instance.digital_object).aggregate(Max('seq_id'))
            biggest_id = '%04d' % (biggest_id['seq_id__max'] + 1)
            instance.seq_id = biggest_id
        except:
            instance.seq_id = '0001'


# Awards
class Award(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"), help_text=_("For a series of awards (e.g. Tony Award, Drama Desk Award), not award categories (Tony Award for Best Musical, etc.)"))
    award_org = models.CharField(max_length=200,  null=True, blank=True, verbose_name=_("award organization"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    website = models.URLField(null=True, blank=True, verbose_name=_("website"))
    
    def has_images(self):
        if DigitalObject.objects.filter(related_award=self, digi_object_format=DigitalObjectType.objects.get(title="Image")).exists():
            return True
        else:
            return False

    def has_videos(self):
        if DigitalObject.objects.filter(related_award=self, digi_object_format=DigitalObjectType.objects.get(title="Video recording"), ready_to_stream=True).exists():
            return True
        else:
            return False

    def has_audio(self):
        if DigitalObject.objects.filter(related_award=self, digi_object_format=DigitalObjectType.objects.get(title="Audio recording")).exists():
            return True
        else:
            return False
    
    def __unicode__(self):
        return "%s" % (self.title)
    
    class Meta:
        ordering = ['title',]

    
class AwardCandidate(models.Model):
    
    award = models.ForeignKey(Award, verbose_name=_("award"))
    year = models.PositiveIntegerField(max_length=4, help_text=_("Please enter a 4-digit year (e.g. 1999, not 99)"), verbose_name=_("year"))
    category = models.CharField(max_length=140, null=True, blank=True, help_text=_("e.g. Best Performance, Best Musical"), verbose_name=_("category"))
    result = models.CharField(max_length=1, choices=constants.AWARD_RESULT_CHOICES, verbose_name=_("result"))
    recipient = models.ForeignKey(Creator, null=True, blank=True, related_name="recipient", help_text=_("A specific person or organization receiving the award"), verbose_name=_("recipient"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    production = models.ForeignKey(Production, null=True, blank=True, default=None, related_name="production", verbose_name=_("production"))
    place = models.ForeignKey("City", null=True, blank=True, default=None, related_name="place", verbose_name=_("City"))
    festival = models.ForeignKey(Festival, null=True, blank=True, default=None, related_name="festival", verbose_name=_("festival"))
    work_record = models.ForeignKey(WorkRecord, null=True, blank=True, default=None, related_name="work_record", verbose_name=_("work record"))
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    profiler_name = models.CharField(max_length=255, null=True, blank=True, default='', verbose_name=_("profiler name"))
    profiler_entry_date = models.CharField(max_length=255, null=True, blank=True, default='', verbose_name=_("profile entry date"))
    
    def __unicode__(self):
        return "%s for %s, %d, %s (%s)" % (self.award.title, self.category, self.year, self.recipient.display_name(), self.get_result_display())
    
    def has_images(self):
        if DigitalObject.objects.filter(related_award=self, digi_object_format=DigitalObjectType.objects.get(title="Image")).exists():
            return True
        else:
            return False

    def has_videos(self):
        if DigitalObject.objects.filter(related_award=self, digi_object_format=DigitalObjectType.objects.get(title="Video recording"), ready_to_stream=True).exists():
            return True
        else:
            return False

    def has_audio(self):
        if DigitalObject.objects.filter(related_award=self, digi_object_format=DigitalObjectType.objects.get(title="Audio recording")).exists():
            return True
        else:
            return False
    
    class Meta:
        ordering = ['award', 'year']


class DigitalObject(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    ascii_title = models.CharField(max_length=255, verbose_name=_("ASCII title"))
    title_variants = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("title variants"))
    collection = models.ForeignKey(Collection, related_name="collection_objects", verbose_name=_("collection"))
    object_creator = models.ForeignKey(Creator, null=True, blank=True, related_name="objects_created", verbose_name=_("object creator"))
    language = models.ManyToManyField("Language", null=True, blank=True, verbose_name=_("language"), related_name="language_objects")
    subject = models.ManyToManyField(SubjectHeading, null=True, blank=True, related_name="collection_objects", verbose_name=_("subject"))
    object_id = models.CharField(max_length=6, null=True, blank=True, verbose_name=_("object ID"))
    digital_id = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("digital ID"))
    rights_holders = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("rights holder(s)"))
    license_type = models.ForeignKey("License", default=1, verbose_name=_("license type"))
    permission_form = models.FileField(upload_to='permissionforms', verbose_name=_("permission form"), null=True, blank=True)
    # Physical object info
    identifier = models.CharField(max_length=60, help_text=_("e.g. ISBN, ISSN, DOI"), null=True, blank=True, verbose_name=_("identifier"))
    marks = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_("marks/inscriptions"))
    measurements = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("physical description"))
    phys_object_type = models.ForeignKey("PhysicalObjectType", verbose_name=_("Physical object type"), related_name="digital_objects", null=True, blank=True)
    donor = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("donor"))
    sponsor_note = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("sponsor note"))
    phys_obj_date = models.DateField(null=True, blank=True, verbose_name=_("physical object date"))
    phys_obj_precision = models.CharField(max_length=1, choices=constants.DATE_PRECISION_CHOICES, default=u'f', null=True, blank=True, verbose_name=_("Precision"))
    phys_obj_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
#    phys_obj_location = models.ForeignKey("Location", null=True, blank=True, verbose_name=_("physical object location"))
    phys_obj_city = models.ForeignKey("City", null=True, blank=True, verbose_name=_("Physical object city"))
    # Digital object info
    digi_object_format = models.ForeignKey("DigitalObjectType", verbose_name=_("Digital object format"), null=True, blank=True)
    # Container info
    series_num = models.CharField(max_length=12, null=True, blank=True, verbose_name=_("series #"))
    series_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("series name"))
    subseries_num = models.CharField(max_length=12, null=True, blank=True, verbose_name=_("subseries #"))
    subseries_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("subseries name"))
    box_num = models.CharField(max_length=12, null=True, blank=True, verbose_name=_("box #"))
    folder_num = models.CharField(max_length=12, null=True, blank=True, verbose_name=_("folder #"))
    drawer_num = models.CharField(max_length=12, null=True, blank=True, verbose_name=_("drawer #"))
    folder_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("folder name"))
    folder_date = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("folder date"))
    # Relationships
    related_production = models.ManyToManyField(Production, related_name="related_production", null=True, blank=True, verbose_name=_("related production"))
    related_festival = models.ManyToManyField(FestivalOccurrence, related_name="related_festival", null=True, blank=True, verbose_name=_("related festival"))
    related_award = models.ManyToManyField(AwardCandidate, related_name="related_award", null=True, blank=True, verbose_name=_("related award"))
    related_venue = models.ManyToManyField(Location, related_name="related_venue", null=True, blank=True, verbose_name=_("related venue"))
    related_creator = models.ManyToManyField(Creator, through="DigitalObject_Related_Creator", related_name="related_creator", null=True, blank=True, verbose_name=_("related creator"))
    related_work = models.ManyToManyField(WorkRecord, related_name="related_work", null=True, blank=True, verbose_name=_("related work"))
    # extra details
    summary = models.TextField(null=True, blank=True, verbose_name=_("summary"))
    notes = models.TextField(null=True, blank=True, verbose_name=_("notes"))
    creation_date = models.DateField(null=True, blank=True, help_text="Click 'Today' to see today's date in the proper date format.", verbose_name=_("creation date"))
    creation_date_precision = models.CharField(max_length=1, null=True, blank=True, choices=constants.DATE_PRECISION_CHOICES, default=u'y', verbose_name=_("Precision"))
    creation_date_BC = models.BooleanField(default=False, verbose_name=_("Is B.C. date"))
    restricted = models.BooleanField(default=False, verbose_name=_("Restricted?"))
    restricted_description = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Details of restrictions"))
    ready_to_stream = models.BooleanField(default=False, verbose_name=_("Uploaded to streaming server"))
    hi_def_video = models.BooleanField(default=False, verbose_name=_("Hi-def video"))
    poster_image = models.FileField(upload_to='digitalobjects/poster_images', storage=OverwriteStorage(), verbose_name=_("Poster image (for videos)"), null=True, blank=True)
    attention = models.TextField(null=True, blank=True, verbose_name=_("attention"))
    has_attention = models.BooleanField(default=False)
    needs_editing = models.BooleanField(default=True, verbose_name=_("needs editing"))
    published = models.BooleanField(default=True, verbose_name=_("published"))
    tags = TaggableManager(verbose_name="Tags", help_text="A comma-separated list of tags.", blank=True) 
 
    def phys_obj_date_display(self):
        return display_date(self.phys_obj_date, self.phys_obj_precision, self.phys_obj_BC)
    
    def creation_date_display(self):
        return display_date(self.creation_date, self.creation_date_precision, self.creation_date_BC)

    def has_related_things(self):
        if self.related_production.exists():
            return True
        if self.related_festival.exists():
            return True
        if self.related_venue.exists():
            return True
        if self.related_creator.exists():
            return True
        if self.related_work.exists():
            return True
        return False

    def object_number(self):
        num = ''
        num += self.collection.repository.repository_id
        num += self.collection.collection_id
        num += self.object_id
        return num

    def object_number_display(self):
        num = ''
        num += self.collection.repository.repository_id + '-'
        num += self.collection.collection_id + '-'
        num += self.object_id
        return num
    
    object_number_display.short_description = _('Digital object number')
    
    def first_file(self):
        if self.files:
          df = self.files.order_by('seq_id')[0]
          return df
        else:
          return False

    def __unicode__(self):
        return "%s (%s)" % (self.title, str(self.object_number()))

    class Meta:
        ordering = ['-collection__repository__repository_id', '-collection__collection_id', '-object_id']

def update_digital_object_title(sender, **kwargs):
    obj = kwargs['instance']
    obj.ascii_title = unidecode(obj.title)

pre_save.connect(update_digital_object_title, sender=DigitalObject)


class DigitalObject_Related_Creator(models.Model):
    
    class Meta:
        verbose_name = _("Related Creators - Digital object")
        verbose_name_plural = _("Related Creators - Digital object")
    
    creator = models.ForeignKey(Creator, verbose_name=_("creator"))
    digitalobject = models.ForeignKey(DigitalObject, verbose_name=_("digital object"))
    
    def __unicode__(self):
        return "%s (%s)" % (self.digitalobject.title, str(self.digitalobject.object_number())) 


class License(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    description = models.TextField(verbose_name=_("description"))
    more_info_link = models.CharField(max_length=255, verbose_name=_("link for more info"))
    image = models.FileField(upload_to='license_images', verbose_name=_("image"), null=True, blank=True)

    def __unicode__(self):
        return self.title

class DigitalObjectType(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    category = models.CharField(max_length=50, verbose_name=_("category"))
    
    def __unicode__(self):
        return self.title
    
class DigitalFile(models.Model):
    filepath = models.FileField(upload_to=object_upload_path, storage=OverwriteStorage(), verbose_name=_("File"), null=True, blank=True)
    seq_id = models.CharField(max_length=4, null=True, blank=True, verbose_name=_("sequence ID"))
    digital_object = models.ForeignKey(DigitalObject, related_name="files", verbose_name=_("digital object"))
    
    def __unicode__(self):
        return self.filepath.name
    
pre_save.connect(setup_new_object, sender=DigitalObject)
pre_save.connect(setup_digital_file, sender=DigitalFile)
    
# Enumeration fields - countries, languages, functions, etc.
class Country(models.Model):
    name = models.CharField(max_length=100, help_text=_("Name of the country (e.g. Cuba)"), verbose_name=_("name"))
    demonym = models.CharField(max_length=100, help_text=_("What someone from this country is called (e.g. Cuban)"), verbose_name=_("demonym"))
    
    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    state = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("state"))
    country = models.ForeignKey(Country, related_name="cities", verbose_name=_("country"))
    
    class Meta:
        verbose_name = _("city")
        verbose_name_plural = _("cities")
        ordering = ['name']
    
    def __unicode__(self):
        if self.state:
            return "%s, %s, %s" % (self.name, self.state, self.country.name)
        else:
            return "%s, %s" % (self.name, self.country.name)

class Language(models.Model):
    name = models.CharField(max_length=60, verbose_name=_("name"))
    shortcode = models.CharField(max_length=2, help_text=_("This language's 2-letter shortcode ('en', 'es', etc.)"), verbose_name=_("shortcode"))
    archival_code = models.CharField(max_length=10, help_text=_("A longer archival language code ('eng', 'spa', etc.)"), verbose_name=_("archival code"))
    
    class Meta:
        verbose_name=_("language")
        verbose_name_plural=_("languages")
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class WorkRecordType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    
    class Meta:
        verbose_name = _("work record type")
        verbose_name_plural = _("work record types")
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class WorkRecordFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("work record function")
        verbose_name_plural = _("work record functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title
        
class DirectingTeamFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("directing team function")
        verbose_name_plural = _("directing team functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title
        
class CastMemberFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("cast member function")
        verbose_name_plural = _("cast member functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title
        
class DesignTeamFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("design team function")
        verbose_name_plural = _("design team functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title
        
class TechTeamFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("technical team function")
        verbose_name_plural = _("technical team functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title

class ProductionTeamFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("production team function")
        verbose_name_plural = _("production team functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title

class DocumentationTeamFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("documentation team function")
        verbose_name_plural = _("documentation team functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title

class AdvisoryTeamFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("advisory team function")
        verbose_name_plural = _("advisory team functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title

class OrgFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    func_type = models.CharField(max_length=6, choices=constants.CREATOR_RELATIONSHIP_TYPES, verbose_name=_("function type"))
    ordinal = models.SmallIntegerField(default=0,null=False, verbose_name=_("Display Order"),
                                       help_text=_("Use to list Related Creator by function ordinal"),) 
    
    class Meta:
        verbose_name = _("organizational function")
        verbose_name_plural = _("organizational functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title
        
class FestivalFunction(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("festival function")
        verbose_name_plural = _("festival functions")
        ordering = ['title']
    
    def __unicode__(self):
        return self.title

class PhysicalObjectType(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    slug = models.CharField(max_length=200, verbose_name=_("slug"), help_text=_("Enter a unique, all-lowercase title (no spaces) for use in URLs."))

    class Meta:
        verbose_name = _("physical object type")
        verbose_name_plural = _("physical object types")
        ordering = ['title']

    # Function to test if this object type has viewable digital objects.
    def has_viewable_objects(self):
        return self.digital_objects.filter(Q(published=True), Q(digi_object_format__title="Image", files__isnull=False) | Q(digi_object_format__title="Video recording", ready_to_stream=True)).exists()

    def __unicode__(self):
        return self.title

class VenueType(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    
    class Meta:
        verbose_name = _("venue type")
        verbose_name_plural = _("venue types")
        ordering = ['title']

    def __unicode__(self):
        return self.title
    

"""    
class BibliographicRecord(models.Model):

    bib_type = models.CharField(max_length=5, choices=constants.BIB_TYPE_CHOICES, verbose_name=_("bibliography type"))
    abstract = models.TextField(null=True, blank=True, verbose_name=_("abstract"))
    title = models.CharField(max_length=255, verbose_name=_("title"))
    short_title = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("short title"))
    booktitle = models.CharField(max_length=255, null=True, blank=True, help_text=_("Only for works contained in a larger book"), verbose_name=_("book title"))
    publication = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("publication title"))
    url = models.URLField(null=True, blank=True, verbose_name=_("URL"))
    author = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("author(s)"))
    editor = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("editor(s)"))
    translator = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("translator(s)"))
    volume = models.CharField(max_length=40, null=True, blank=True, verbose_name=_("volume"))
    num_volumes = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("number of volumes"))
    issue_num = models.CharField(max_length=40, null=True, blank=True, help_text=_("Issue number"), verbose_name=_("issue number"))
    series = models.CharField(max_length=255, null=True, blank=True, help_text=_("Series title"), verbose_name=_("series"))
    series_text = models.CharField(max_length=255, null=True, blank=True, help_text=_("Series subtitle"), verbose_name=_("series text"))
    series_num = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("series number"))
    chapter = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("chapter"))
    edition = models.CharField(max_length=30, null=True, blank=True, help_text=_("Enter as an ordinal number ('Second', 'Third')"), verbose_name=_("edition"))
    section = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("section"))
    pub_date = models.CharField(max_length=120, null=True, blank=True, verbose_name=_("publication date"))
    access_date = models.CharField(max_length=120, null=True, blank=True, verbose_name=_("access date"))
    num_pages = models.CharField(max_length=60, null=True, blank=True, verbose_name=_("number of pages"))
    language = models.CharField(max_length=60, null=True, blank=True, verbose_name=_("language"))
    isbn = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("ISBN"))
    issn = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("ISSN"))
    doi = models.CharField(max_length=80, null=True, blank=True, verbose_name=_("DOI"))
    pages = models.CharField(max_length=30, null=True, blank=True, help_text=_("Enter one or more pages / page ranges"), verbose_name=_("pages"))
    publisher = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("publisher"))
    address = models.CharField(max_length=255, null=True, blank=True, help_text=_("Publisher's address; omit for major publishers"), verbose_name=_("address"))
    medium = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("medium"))
    format = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("format"))
    art_size = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("artwork size"))
    label = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("label"))
    runtime = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("running time"))
    archive = models.CharField(max_length=255, null=True, blank=True, help_text=_("An archive that holds this item"), verbose_name=_("archive"))
    archive_location = models.CharField(max_length=200, null=True, blank=True, help_text=_("A call number or location within the archive holding this item"), verbose_name=_("location in archive"))
    version = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("version"))
    system = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("system"))
    type = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("type"))
    university = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("university"))
    library = models.CharField(max_length=255, null=True, blank=True, help_text=_("A library that holds this item"), verbose_name=_("library"))
    library_catalog_num = models.CharField(max_length=255, null=True, blank=True, help_text=_("The catalog call number for the library holding this item"), verbose_name=_("library catalog number"))
    rights = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("rights"))
    extra = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("extra"))
    work_record = models.ForeignKey("WorkRecord", null=True, blank=True, verbose_name=_("work record"))
    tags = TaggableManager(verbose_name="Tags", help_text="A comma-separated list of tags.", blank=True)
    
    class Meta:
        verbose_name = _("bibliographic record")
        verbose_name_plural = _("bibliographic records")
    
    def __unicode__(self):
        if self.journal:
            return "%s, %s. %s. %s" % (self.author, self.title, self.journal, self.year)
        else:
            return "%s, %s (%s)" % (self.author, self.title, self.year)

class BibliographicRecordType(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    has_abstract = models.BooleanField(default=True, verbose_name=_("has an abstract"))
    has_title = models.BooleanField(default=True, verbose_name=_("has a title"))
    has_shorttitle = models.BooleanField(default=False, verbose_name=_("has a short title"))
    has_booktitle = models.BooleanField(default=False, verbose_name=_("has a book title"))
    has_pubtitle = models.BooleanField(default=False, verbose_name=_("has a publication title"))
    has_url = models.BooleanField(default=False, verbose_name=_("has a URL"))
    has_author = models.BooleanField(default=True, verbose_name=_("has an author / creator"))
    has_editor = models.BooleanField(default=False, verbose_name=_("has an editor"))
    has_translator = models.BooleanField(default=False, verbose_name=_("has a translator"))
    has_volume = models.BooleanField(default=False, verbose_name=_("has a volume number"))
    has_num_volumes = models.BooleanField(default=False, verbose_name=_("has a fixed number of volumes"))
    has_issue_num = models.BooleanField(default=False, verbose_name=_("has an issue number"))
    has_series = models.BooleanField(default=False, verbose_name=_("has a book series title"))
    has_chapter = models.BooleanField(default=False, verbose_name=_("has chapter numbers"))
    has_edition = models.BooleanField(default=False, verbose_name=_("has editions"))
    has_month = models.BooleanField(default=False, verbose_name=_("has a month designation"))
    has_year = models.BooleanField(default=False, verbose_name=_("has a year designation"))
    has_pages = models.BooleanField(default=False, verbose_name=_("has a page range / ranges"))
    has_publisher = models.BooleanField(default=False, verbose_name=_("has a publisher"))
    has_address = models.BooleanField(default=False, verbose_name=_("has a publisher's address"))
    has_workrecord = models.BooleanField(default=False, verbose_name=_("is linked to a work record"))
"""

class TranslatingFlatPage(FlatPage):
    order = models.IntegerField(default=0, verbose_name=_("page order"), help_text=_("Where in the list this page should show up - 0 comes first, then 1, etc."))
    child_of = models.ForeignKey('TranslatingFlatPage', null=True, blank=True, default=None, verbose_name=_("child of"), related_name="flatpage_parent", help_text=_("This page's parent, if any"))
    class Meta:
        verbose_name = _("Static page")

class HomePageInfo(models.Model):
    if settings.PYTHON_OLDER_THAN_27:
        BOX_CHOICES = [ (0, '0 (no textbox)'), (1, '1'), (2, '2'), (3, '3') ]
    else:
        BOX_CHOICES = { (0, '0 (no textbox)'), (1, '1'), (2, '2'), (3, '3') }
        
    content = models.TextField(verbose_name=_("textbox content"), null=True, blank=True)
    num_boxes = models.SmallIntegerField(choices=BOX_CHOICES, default=0, verbose_name=_("Number of boxes"), help_text=_("How many image boxes the textbox should replace"))
    box_1_id = models.IntegerField(null=True, blank=True, verbose_name=_("Digital object for box 1"), help_text=_("Enter the ID number of the digital object that should go here."))
    box_2_id = models.IntegerField(null=True, blank=True, verbose_name=_("Digital object for box 2"), help_text=_("Enter the ID number of the digital object that should go here."))
    box_3_id = models.IntegerField(null=True, blank=True, verbose_name=_("Digital object for box 3"), help_text=_("Enter the ID number of the digital object that should go here."))
    
    class Meta:
        verbose_name = _("Home page settings")
    
    def __unicode__(self):
        return "Home page settings (DO NOT DELETE)"

# register version control
# reversion.register(Creator)
# reversion.register(Location)
# reversion.register(WorkRecord)
# reversion.register(Production)
# reversion.register(FestivalOccurrence)
# reversion.register(DigitalObject)
