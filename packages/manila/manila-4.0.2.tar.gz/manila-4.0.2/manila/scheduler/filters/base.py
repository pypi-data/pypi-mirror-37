# Copyright (c) 2011-2012 OpenStack Foundation.
# All Rights Reserved.
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

"""
Filter support
"""
from oslo_log import log

from manila.i18n import _LI
from manila.scheduler import base_handler

LOG = log.getLogger(__name__)


class BaseFilter(object):
    """Base class for all filter classes."""
    def _filter_one(self, obj, filter_properties):
        """Check if an object passes a filter.

        Return True if it passes the filter, False otherwise.
        Override this in a subclass.
        """
        return True

    def filter_all(self, filter_obj_list, filter_properties):
        """Yield objects that pass the filter.

        Can be overridden in a subclass, if you need to base filtering
        decisions on all objects.  Otherwise, one can just override
        _filter_one() to filter a single object.
        """
        for obj in filter_obj_list:
            if self._filter_one(obj, filter_properties):
                yield obj

    # Set to true in a subclass if a filter only needs to be run once
    # for each request rather than for each instance
    run_filter_once_per_request = False

    def run_filter_for_index(self, index):
        """Check if filter needs to be run for the "index-th" instance.

        Return True if the filter needs to be run for the "index-th"
        instance in a request.  Only need to override this if a filter
        needs anything other than "first only" or "all" behaviour.
        """
        return not (self.run_filter_once_per_request and index > 0)


class BaseFilterHandler(base_handler.BaseHandler):
    """Base class to handle loading filter classes.

    This class should be subclassed where one needs to use filters.
    """

    def get_filtered_objects(self, filter_classes, objs,
                             filter_properties, index=0):
        """Get objects after filter

        :param filter_classes: filters that will be used to filter the
                               objects
        :param objs: objects that will be filtered
        :param filter_properties: client filter properties
        :param index: This value needs to be increased in the caller
                      function of get_filtered_objects when handling
                      each resource.
        """
        list_objs = list(objs)
        LOG.debug("Starting with %d host(s)", len(list_objs))
        for filter_cls in filter_classes:
            cls_name = filter_cls.__name__
            filter_class = filter_cls()

            if filter_class.run_filter_for_index(index):
                objs = filter_class.filter_all(list_objs, filter_properties)
                if objs is None:
                    LOG.debug("Filter %(cls_name)s says to stop filtering",
                              {'cls_name': cls_name})
                    return
                list_objs = list(objs)
                msg = (_LI("Filter %(cls_name)s returned %(obj_len)d host(s)")
                       % {'cls_name': cls_name, 'obj_len': len(list_objs)})
                if not list_objs:
                    LOG.info(msg)
                    break
                LOG.debug(msg)
        return list_objs
