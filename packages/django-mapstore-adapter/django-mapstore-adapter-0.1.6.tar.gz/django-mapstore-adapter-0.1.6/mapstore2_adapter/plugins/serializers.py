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

from __future__ import absolute_import

from ..api.models import (MapStoreData,
                          MapStoreAttribute)

from rest_framework.exceptions import APIException

try:
    import json
except ImportError:
    from django.utils import simplejson as json

import base64
import logging
import traceback

logger = logging.getLogger(__name__)


class GeoNodeSerializer(object):

    @classmethod
    def update_data(cls, serializer, data):
        if data:
            _data, created = MapStoreData.objects.get_or_create(
                resource=serializer.instance)
            _data.resource = serializer.instance
            _data.blob = data
            _data.save()
            serializer.validated_data['data'] = _data

    @classmethod
    def update_attributes(cls, serializer, attributes):
        _attributes = []
        for _a in attributes:
            attribute, created = MapStoreAttribute.objects.get_or_create(
                name=_a['name'],
                resource=serializer.instance)
            attribute.resource = serializer.instance
            attribute.name = _a['name']
            attribute.type = _a['type']
            attribute.label = _a['label']
            attribute.value = base64.encodestring(_a['value'].encode('utf8'))
            attribute.save()
            _attributes.append(attribute)
        serializer.validated_data['attributes'] = _attributes

    def get_queryset(self, caller, queryset):
        allowed_map_ids = []
        for _q in queryset:
            mapid = _q.id
            try:
                from geonode.maps.views import (_resolve_map,
                                                _PERMISSION_MSG_VIEW)
                map_obj = _resolve_map(
                    caller.request,
                    str(mapid),
                    'base.view_resourcebase',
                    _PERMISSION_MSG_VIEW)
                if map_obj:
                    allowed_map_ids.append(mapid)
            except BaseException:
                tb = traceback.format_exc()
                logger.error(tb)

        # queryset = queryset.filter(user=self.request.user)
        queryset = queryset.filter(id__in=allowed_map_ids)
        return queryset

    def get_geonode_map(self, caller, serializer):
        from geonode.maps.views import _PERMISSION_MSG_SAVE
        try:
            from geonode.maps.views import _resolve_map
            if 'id' in serializer.validated_data:
                mapid = serializer.validated_data['id']
                map_obj = _resolve_map(
                    caller.request,
                    str(mapid),
                    'base.change_resourcebase',
                    _PERMISSION_MSG_SAVE)
                return map_obj
        except BaseException:
            tb = traceback.format_exc()
            logger.error(tb)
            raise APIException(_PERMISSION_MSG_SAVE)

    def set_geonode_map(self, caller, serializer, map_obj=None, data=None, attributes=None):

        def decode_base64(data):
            """Decode base64, padding being optional.

            :param data: Base64 data as an ASCII byte string
            :returns: The decoded byte string.

            """
            _thumbnail_format = 'png'
            _invalid_padding = data.find(';base64,')
            if _invalid_padding:
                _thumbnail_format = data[data.find('image/') + len('image/'):_invalid_padding]
                data = data[_invalid_padding + len(';base64,'):]
            missing_padding = len(data) % 4
            if missing_padding != 0:
                data += b'=' * (4 - missing_padding)
            return (data.decode('base64'), _thumbnail_format)

        _map_name = None
        _map_title = None
        _map_abstract = None
        _map_thumbnail = None
        _map_thumbnail_format = 'png'
        if attributes:
            for _a in attributes:
                if _a['name'] == 'name':
                    _map_name = _a['value']
                if _a['name'] == 'title':
                    _map_title = _a['value']
                if _a['name'] == 'abstract':
                    _map_abstract = _a['value']
                if 'thumb' in _a['name']:
                    (_map_thumbnail, _map_thumbnail_format) = decode_base64(_a['value'])
        elif map_obj:
            _map_title = map_obj.title
            _map_abstract = map_obj.abstract

        _map_name = _map_name or None
        if not _map_name and 'name' in serializer.validated_data:
            _map_name = serializer.validated_data['name']
        _map_title = _map_title or _map_name
        _map_abstract = _map_abstract or ""
        if data:
            try:
                _map_conf = dict(data)
                _map_conf["about"] = {
                    "name": _map_name,
                    "title": _map_title,
                    "abstract": _map_abstract}
                _map_conf['sources'] = {}
                from geonode.layers.views import layer_detail
                _map_obj = data.pop('map', None)
                if _map_obj:
                    for _lyr in _map_obj['layers']:
                        _lyr_context = None
                        try:
                            # Retrieve the Layer Params back from GeoNode
                            _gn_layer = layer_detail(
                                caller.request,
                                _lyr['name'])
                            if _gn_layer and _gn_layer.context_data:
                                _context_data = json.loads(_gn_layer.context_data['viewer'])
                                for _gn_layer_ctx in _context_data['map']['layers']:
                                    if 'name' in _gn_layer_ctx and _gn_layer_ctx['name'] == _lyr['name']:
                                        _lyr_context = _gn_layer_ctx
                                        _src_idx = _lyr_context['source']
                                        _map_conf['sources'][_src_idx] = _context_data['sources'][_src_idx]
                        except BaseException:
                            tb = traceback.format_exc()
                            logger.error(tb)
                        # Store ms2 layer id
                        if "id" in _lyr and _lyr["id"]:
                             _lyr['extraParams'] = {"msId": _lyr["id"]}

                        # Store the Capabilities Document into the Layer Params of GeoNode
                        if _lyr_context:
                            if 'capability' in _lyr_context:
                                _lyr['capability'] = _lyr_context['capability']
                        elif 'source' in _lyr:
                            _map_conf['sources'][_lyr['source']] = {}

                    if not map_obj:
                        # Create a new GeoNode Map
                        from geonode.maps.models import Map
                        map_obj = Map(
                            title=_map_title,
                            owner=caller.request.user,
                            center_x=_map_obj['center']['x'],
                            center_y=_map_obj['center']['y'],
                            zoom=_map_obj['zoom'])
                        map_obj.save()

                    # Update GeoNode Map
                    _map_conf['map'] = _map_obj
                    map_obj.update_from_viewer(
                        _map_conf,
                        context={'config': _map_conf})

                    # Dumps thumbnail from MapStore2 Interface
                    if _map_thumbnail:
                        _map_thumbnail_filename = "map-%s-thumb.%s" % (map_obj.uuid, _map_thumbnail_format)
                        map_obj.save_thumbnail(_map_thumbnail_filename, _map_thumbnail)

                    serializer.validated_data['id'] = map_obj.id
                    serializer.save(user=caller.request.user)
            except BaseException:
                tb = traceback.format_exc()
                logger.error(tb)
                raise APIException(tb)
        else:
            raise APIException("Map Configuration (data) is Mandatory!")

    def perform_create(self, caller, serializer):
        map_obj = self.get_geonode_map(caller, serializer)

        _data = None
        _attributes = None

        if 'data' in serializer.validated_data:
            _data = serializer.validated_data.pop('data', None)
        else:
            raise APIException("Map Configuration (data) is Mandatory!")

        if 'attributes' in serializer.validated_data:
            _attributes = serializer.validated_data.pop('attributes', None)
        else:
            raise APIException("Map Metadata (attributes) are Mandatory!")

        self.set_geonode_map(caller, serializer, map_obj, _data, _attributes)

        if _data:
            # Save JSON blob
            GeoNodeSerializer.update_data(serializer, _data)

        if _attributes:
            # Sabe Attributes
            GeoNodeSerializer.update_attributes(serializer, _attributes)

        return serializer.save()

    def perform_update(self, caller, serializer):
        map_obj = self.get_geonode_map(caller, serializer)

        _data = None
        _attributes = None

        if 'data' in serializer.validated_data:
            _data = serializer.validated_data.pop('data', None)

            # Save JSON blob
            GeoNodeSerializer.update_data(serializer, _data)

        if 'attributes' in serializer.validated_data:
            _attributes = serializer.validated_data.pop('attributes', None)

            # Sabe Attributes
            GeoNodeSerializer.update_attributes(serializer, _attributes)

        self.set_geonode_map(caller, serializer, map_obj, _data, _attributes)

        return serializer.save()
