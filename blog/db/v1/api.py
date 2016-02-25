# Copyright 2015 - Mirantis, Inc.
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

import contextlib

from oslo.db import api as db_api

from blog.openstack.common import log as logging

_BACKEND_MAPPING = {
    'sqlalchemy': 'blog.db.v1.sqlalchemy.api',
}

IMPL = db_api.DBAPI('sqlalchemy', backend_mapping=_BACKEND_MAPPING)
LOG = logging.getLogger(__name__)


def setup_db():
    IMPL.setup_db()


def drop_db():
    IMPL.drop_db()


# Transaction control.


def start_tx():
    IMPL.start_tx()


def commit_tx():
    IMPL.commit_tx()


def rollback_tx():
    IMPL.rollback_tx()


def end_tx():
    IMPL.end_tx()


@contextlib.contextmanager
def transaction():
    with IMPL.transaction():
        yield


# Locking.


def acquire_lock(model, id):
    IMPL.acquire_lock(model, id)


# Workbooks.

def get_blog(title):
    return IMPL.get_blog(title)


def load_blog(title):
    """Unlike get_blog this method is allowed to return None."""
    return IMPL.load_blog(title)


def get_blogs():
    return IMPL.get_blogs()


def create_blog(values):
    return IMPL.create_blog(values)


def update_blog(title, values):
    return IMPL.update_blog(title, values)


def create_or_update_blog(title, values):
    return IMPL.create_or_update_blog(title, values)


def delete_blog(title):
    IMPL.delete_blog(title)


def delete_blogs(**kwargs):
    IMPL.delete_blogs(**kwargs)
