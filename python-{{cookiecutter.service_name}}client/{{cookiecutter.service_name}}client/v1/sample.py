# -*- coding: utf-8 -*-
#
# Copyright © 2013 Red Hat, Inc
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from {{cookiecutter.service_name}}client.common import base
from {{cookiecutter.service_name}}client.common import utils
from {{cookiecutter.service_name}}client import exc


CREATION_ATTRIBUTES = ['description', 'extra']


class Sample(base.Resource):
    def __repr__(self):
        return "<Sample %s>" % self._info


class SampleManager(base.Manager):
    resource_class = Sample

    @staticmethod
    def _path(id=None):
        return '/v1/sample/%s' % id if id else '/v1/sample'

    def list(self, limit=None, sort_key=None,
             sort_dir=None, detail=False):
        """Retrieve a list of sample.
        :param limit: The maximum number of results to return per
                      request, if:
            1) limit > 0, the maximum number of sample to return.
            2) limit == 0, return the entire list of sample.
            3) limit param is NOT specified (None), the number of items
               returned respect the maximum imposed by the Ironic API
               (see Ironic's api.max_limit option).
        :param sort_key: Optional, field used for sorting.
        :param sort_dir: Optional, direction of sorting, either 'asc' (the
                         default) or 'desc'.
        :param detail: Optional, boolean whether to return detailed information
                       about sample.
        :returns: A list of sample.
        """
        if limit is not None:
            limit = int(limit)

        filters = utils.common_filters(marker, limit, sort_key, sort_dir)

        path = ''
        if detail:
            path += 'detail'
        if filters:
            path += '?' + '&'.join(filters)

        if limit is None:
            return self._list(self._path(path), "sample")
        else:
            return self._list_pagination(self._path(path), "sample",
                                         limit=limit)

    def list_children(self, sample_id, limit=None,
                   sort_key=None, sort_dir=None, detail=False):
        """List all the children for a given sample.
        :param sample_id: The UUID of the sample.
        :param limit: The maximum number of results to return per
                      request, if:
            1) limit > 0, the maximum number of children to return.
            2) limit == 0, return the entire list of children.
            3) limit param is NOT specified (None), the number of items
               returned respect the maximum imposed by the Ironic API
               (see Ironic's api.max_limit option).
        :param sort_key: Optional, field used for sorting.
        :param sort_dir: Optional, direction of sorting, either 'asc' (the
                         default) or 'desc'.
        :param detail: Optional, boolean whether to return detailed information
                       about children.
        :returns: A list of children.
        """
        if limit is not None:
            limit = int(limit)

        filters = utils.common_filters(marker, limit, sort_key, sort_dir)

        path = "%s/children" % sample_id
        if detail:
            path += '/detail'

        if filters:
            path += '?' + '&'.join(filters)

        if limit is None:
            return self._list(self._path(path), "children")
        else:
            return self._list_pagination(self._path(path), "children",
                                         limit=limit)

    def get(self, sample_id):
        try:
            return self._list(self._path(sample_id))[0]
        except IndexError:
            return None

    def create(self, **kwargs):
        new = {}
        for (key, value) in kwargs.items():
            if key in CREATION_ATTRIBUTES:
                new[key] = value
            else:
                raise exc.InvalidAttribute()
        return self._create(self._path(), new)

    def delete(self, sample_id):
        return self._delete(self._path(sample_id))

    def update(self, sample_id, patch):
        return self._update(self._path(sample_id), patch)

