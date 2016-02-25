# Copyright 2013 - Mirantis, Inc.
# Copyright 2015 - StackStorm, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import time
import pecan
from pecan import hooks
from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from blog.api.controllers import resource
from blog.api.controllers.v1 import validation
from blog.api.hooks import content_type as ct_hook
from blog.db.v1 import api as db_api
from blog.openstack.common import log as logging
from blog.utils import rest_utils


LOG = logging.getLogger(__name__)


class Blog(resource.Resource):
    """Blog resource."""

    id = wtypes.text
    title = wtypes.text


    content = wtypes.text
    creator = wtypes.text

    created_time = wtypes.text
    updated_time = wtypes.text

    @classmethod
    def sample(cls):
        return cls(id='123e4567-e89b-12d3-a456-426655440000',
                   title='openstack study',
                   content='This is my first blog from openstack',
                   creator='stephen',
                   created_time='1970-01-01T00:00:00.000000',
                   updated_time='1970-01-01T00:00:00.000000')


class Blogs(resource.Resource):
    """A collection of Blogs."""

    blogs = [Blog]

    @classmethod
    def sample(cls):
        return cls(blogs=[Blog.sample()])


class JSONObject:
    def __init__(self,d):
        self.__dict__ =d


class BlogsController(rest.RestController, hooks.HookController):
    __hooks__ = [ct_hook.ContentTypeHook("application/json", ['POST', 'PUT'])]

    @rest_utils.wrap_wsme_controller_exception
    @wsme_pecan.wsexpose(Blog, wtypes.text)
    def get(self, title):
        """Return the title blog."""
        LOG.info("Fetch blog [title=%s]" % title)

        db_model = db_api.get_blog(title)

        return Blog.from_dict(db_model.to_dict())

    @rest_utils.wrap_pecan_controller_exception
    @pecan.expose(content_type="application/json")
    def put(self):
        """Update a blog."""
        definition = pecan.request.text
        print definition
        print type(definition)
        definition = unicode_to_dict(definition)
        LOG.info("Update blog [definition=%s]" % definition)

        blog = db_api.update_blog(definition['title'], definition)


        return Blog.from_dict(blog.to_dict()).to_string()

    @rest_utils.wrap_pecan_controller_exception
    @pecan.expose(content_type="text/plain")
    def post(self):
        """Create a new blog."""
        definition = pecan.request.text

        definition = unicode_to_dict(definition)
        definition['creator'] = 'stephen'

        LOG.info("Create blog [definition=%s]" % definition)

        blog = db_api.create_blog(definition)
        pecan.response.status = 201

        return Blog.from_dict(blog.to_dict()).to_string()


    @rest_utils.wrap_wsme_controller_exception
    @wsme_pecan.wsexpose(None, wtypes.text, status_code=204)
    def delete(self, title):
        """Delete the title blog."""
        LOG.info("Delete blog [title=%s]" % title)

        db_api.delete_blog(title)

    @wsme_pecan.wsexpose(Blogs)
    def get_all(self):
        """Return all blogs.

        Where project_id is the same as the requestor or
        project_id is different but the scope is public.
        """
        LOG.info("Fetch blogs.")

        blogs_list = [Blog.from_dict(db_model.to_dict())
                          for db_model in db_api.get_blogs()]

        return Blogs(blogs=blogs_list)


def unicode_to_dict(definition):
    definition = definition.encode("utf-8")
    dict = {}
    if (len(definition) <= 0):
        return dict
    for str in definition.split('&'):
        dict[str.split('=')[0]] = str.split('=')[1]
    return dict