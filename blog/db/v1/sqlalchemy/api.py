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

import datetime
import contextlib
import sys

from oslo.config import cfg
from oslo.db import exception as db_exc
from oslo.utils import timeutils
import sqlalchemy as sa

from blog.db.sqlalchemy import base as b
from blog.db.sqlalchemy import model_base as mb
from blog.db.sqlalchemy import sqlite_lock
from blog.db.v1.sqlalchemy import models
from blog import exceptions as exc
from blog.openstack.common import log as logging
from blog.services import security
from jsonrpclib.jsonrpc import json

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


def get_backend():
    """Consumed by openstack common code.

    The backend is this module itself.
    :return Name of db backend.
    """
    return sys.modules[__name__]


def setup_db():
    print "------ blog/db/v1/api.setup_db()--46"
    try:
        models.Blog.metadata.create_all(b.get_engine())
    except sa.exc.OperationalError as e:
        raise exc.DBException("Failed to setup database: %s" % e)


def drop_db():
    global _facade

    try:
        models.Blog.metadata.drop_all(b.get_engine())
        _facade = None
    except Exception as e:
        raise exc.DBException("Failed to drop database: %s" % e)


# Transaction management.

def start_tx():
    b.start_tx()


def commit_tx():
    b.commit_tx()


def rollback_tx():
    b.rollback_tx()


def end_tx():
    b.end_tx()


@contextlib.contextmanager
def transaction():
    try:
        start_tx()
        yield
        commit_tx()
    finally:
        end_tx()


@b.session_aware()
def acquire_lock(model, id, session=None):
    if b.get_driver_name() != 'sqlite':
        query = _secure_query(model).filter("id = '%s'" % id)

        query.update(
            {'updated_time': timeutils.utcnow()},
            synchronize_session=False
        )
    else:
        sqlite_lock.acquire_lock(id, session)


def _secure_query(model):
    query = b.model_query(model)

#     if issubclass(model, mb.BlogSecureModelBase):
#         query = query.filter(
#             sa.or_(
# #                 model.project_id == security.get_project_id(),
# #                 model.scope == 'public'
#                 model.project_id == "blo1g",
#                 model.scope == 'private'
#             )
#         )
 
    return query


def _delete_all(model, session=None, **kwargs):
    _secure_query(model).filter_by(**kwargs).delete()


def _get_collection_sorted_by_name(model, **kwargs):
    return _secure_query(model).filter_by(**kwargs).order_by(model.title).all()


def _get_collection_sorted_by_time(model, **kwargs):
    query = _secure_query(model)

    return query.filter_by(**kwargs).order_by(model.created_time).all()


def _get_db_object_by_name(model, title):
    return _secure_query(model).filter_by(title=title).first()


def _get_db_object_by_id(model, id):
    return _secure_query(model).filter_by(id=id).first()


# Workbook definitions.

def get_blog(title):
    blog = _get_blog(title)

    if not blog:
        raise exc.NotFoundException(
            "Blog not found [blog_title=%s]" % title)

    return blog


def load_blog(title):
    return _get_blog(title)


def get_blogs(**kwargs):
    return _get_collection_sorted_by_name(models.Blog, **kwargs)


@b.session_aware()
def create_blog(values, session=None):
    blog = models.Blog()

    now = datetime.datetime.now()
    values['created_time'] = now
    values['updated_time'] = now
    blog.update(values.copy())

    try:
        blog.save(session=session)
    except db_exc.DBDuplicateEntry as e:
        raise exc.DBDuplicateEntry(
            "Duplicate entry for BlogDefinition: %s" % e.columns
        )

    return blog


@b.session_aware()
def update_blog(title, values, session=None):
    wb = _get_blog(title)

    if not wb:
        raise exc.NotFoundException(
            "Blog not found [blog_title=%s]" % title)

    now = datetime.datetime.now()
    values['updated_time'] = now
    wb.update(values.copy())

    return wb


@b.session_aware()
def create_or_update_blog(title, values, session=None):
    if not _get_blog(title):
        return create_blog(values)
    else:
        return update_blog(title, values)


@b.session_aware()
def delete_blog(title, session=None):
    blog = _get_blog(title)

    if not blog:
        raise exc.NotFoundException(
            "Blog not found [blog_title=%s]" % title)

    session.delete(blog)


def _get_blog(title):
    return _get_db_object_by_name(models.Blog, title)


@b.session_aware()
def delete_blogs(**kwargs):
    return _delete_all(models.Blog, **kwargs)
