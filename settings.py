
"""
Copyright (C) 2012  University of Miami
 
This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.
 
This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
 See the GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import os
import sys

gettext = lambda s: s

DEBUG = False
THUMBNAIL_DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Sreeharsha Venkatapuram', 'svenkatapuram@med.miami.edu'),
)

MANAGERS = ADMINS

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'database',                      # Or path to database file if using sqlite3.
#        'USER': 'user',                      # Not used with sqlite3.
#        'PASSWORD': 'password',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}

"""
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
"""

BASE_DIR = os.path.join( os.path.dirname( __file__ ), '..' )
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

SETTINGS_PATH = os.path.dirname( os.path.abspath( __file__ ) )
DEPLOYED_PATH = os.path.join( SETTINGS_PATH, "../" )

# adding the apps directory to the first position of the PYTHON_PATH, but keeping our dir in the top too
sys.path.insert(0, os.path.join(PROJECT_PATH, ''))


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Detroit'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media (uploads, video files, etc.)
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = ''

# Absolute path to the directory that holds static assets (site design, etc.)
#STATICFILES_DIRS = (
#	'/ctda/www/html/static',
#)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://example.com/media/'

#STATIC_URL = 'http://example.com/static/'

#STATIC_ROOT = '/path/to/static'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = 'http://example.com/media/admin/'

# Make this unique, and don't share it with anybody.
#SECRET_KEY = 'w#sjwc#ov(g*a)_b+sa31raerncoi7@5pt@algjc0@9^soqrc*'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'archive.middleware.FlatpageFallbackMiddleware',
)

#INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'urls'

#TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #'/path/to/templates',
#)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.flatpages',
    'sorl.thumbnail',
    'reversion',
    'workflow',
    'modeltranslation',
    'django.contrib.admin',
    'ajax_select',
    'selectable',
    'dajaxice',
    'dajax',
    'rosetta',
    'taggit',
    'taggit_autocomplete_modified',
    'publications',
    'archive',
    'tinymce',
    'haystack',
    'south',
    'disqus',
    'unaccent',
    'rest_framework',
    'api.creators',
    'apps.accounts',
)

DISQUS_API_KEY = 'haO01iiF2PCConCBF0j85S3WQD8eA0tit3XwEOIhqHfZ5g17QFBQEC0uHzBfXgWK'
DISQUS_WEBSITE_SHORTNAME = 'cubantheater'
#TAGGIT_AUTOCOMPLETE_JS_BASE_URL = 'http://ctda.library.miami.edu/media/js'
TAGGIT_AUTOCOMPLETE_JS_BASE_URL = '/static/taggit_autocomplete_modified'

PASSWORD_MINIMUM_LENGTH=6
DAYS_TO_REGISTER = 3

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:8983/solr/collection1'
    },
}


# Modeltranslation settings
LANGUAGES = (
    ('en', gettext('English')),
    ('es', gettext('Spanish')),
)
MODELTRANSLATION_TRANSLATION_REGISTRY = 'archive.translation'

AJAX_LOOKUP_CHANNELS = {
    'creator': ('archive.lookups', 'CreatorLookup'),
    'production': ('archive.lookups', 'ProductionLookup'),
    'festival': dict(model='archive.FestivalOccurrence', search_field='title'),
    'location': ('archive.lookups', 'LocationLookup'),
    'workrecord': ('archive.lookups', 'WorkRecordLookup'),
    'role': ('archive.lookups', 'RoleLookup')
}


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.XMLParser',
    )
}

DEFAULT_LANG = "en"

try:
    from local_settings import *
except ImportError:
    pass
