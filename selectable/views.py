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

from django.core.serializers import json
from django.http import HttpResponse, Http404
from django.utils import simplejson

from selectable.registry import registry


def get_lookup(request, lookup_name):

    lookup_cls = registry.get(lookup_name)
    if lookup_cls is None:
        raise Http404(u'Lookup %s not found' % lookup_name)

    lookup = lookup_cls()
    return lookup.results(request)

