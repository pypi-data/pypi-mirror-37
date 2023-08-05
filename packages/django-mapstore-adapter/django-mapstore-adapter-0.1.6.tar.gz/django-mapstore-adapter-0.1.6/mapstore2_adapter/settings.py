# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright 2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################

from django.conf import settings


# Location of url mappings
PROJECT_NAME = 'mapstore2_adapter'
settings.ROOT_URLCONF = '{}.urls'.format(PROJECT_NAME)

try:
    settings.TEMPLATES[0]['OPTIONS']['context_processors'] += ['mapstore2_adapter.context_processors.resource_urls',]
except:
    pass

try:
    settings.LOGGING["loggers"]["mapstore2_adapter"] = {"handlers": ["console"], "level": "INFO", }
except:
    pass

settings.MAPSTORE2_ADAPTER_SERIALIZER = "mapstore2_adapter.plugins.serializers.GeoNodeSerializer"

MAP_DEBUG = getattr(settings, "MAPSTORE_DEBUG", False)
MAP_BASELAYERS = getattr(settings, "MAPSTORE_BASELAYERS", [])
CATALOGUE_SERVICES = getattr(settings, "MAPSTORE_CATALOGUE_SERVICES", {})
CATALOGUE_SELECTED_SERVICE = getattr(settings, "MAPSTORE_CATALOGUE_SELECTED_SERVICE", None)
