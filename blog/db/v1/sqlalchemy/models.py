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

import hashlib
import json
import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

from blog.db.sqlalchemy import model_base as mb
from blog.db.sqlalchemy import types as st
from blog import utils
from httplib import CREATED


# Definition objects.


class Definition(mb.BlogSecureModelBase):
    __abstract__ = True


# There's no WorkbookExecution so we safely omit "Definition" in the name.
class Blog(Definition):
    """Contains info about blog"""

    __tablename__ = 'blog_v2'

    __table_args__ = (
        sa.UniqueConstraint('title', 'project_id'),
    )

    id = mb.id_column()
    title = sa.Column(sa.String(500))
    content = sa.Column(sa.Text(), nullable=True)
    creator = sa.Column(sa.String(100), nullable=True)
    created_time = sa.Column(sa.DateTime, nullable=True)
    updated_time = sa.Column(sa.DateTime, nullable=True)
    test_alembic = sa.Column(sa.String(100), nullable=True)
    test_alembic123 = sa.Column(sa.String(100), nullable=True)


# Register all hooks related to secure models.
mb.register_secure_model_hooks()
