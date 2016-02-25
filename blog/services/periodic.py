# -*- coding: utf-8 -*-
#
# Copyright 2013 - Mirantis, Inc.
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

from blog import context as auth_ctx
from blog.db.v1 import api as db_api_v2
from blog.engine import rpc
from blog.openstack.common import log
from blog.openstack.common import periodic_task
from blog.openstack.common import threadgroup
from blog.services import security
# from mistral.services import triggers

LOG = log.getLogger(__name__)


class BlogPeriodicTasks(periodic_task.PeriodicTasks):
    @periodic_task.periodic_task(spacing=1, run_immediately=True)
    def process_cron_triggers_v2(self, ctx):
        LOG.debug("Processing cron trigger: %s" % t)
        # Setup admin context before schedule triggers.
        ctx = security.create_context(t.trust_id, t.project_id)
        uth_ctx.set_ctx(ctx)
 
        LOG.debug("Cron trigger security context: %s" % ctx)


def setup():
    tg = threadgroup.ThreadGroup()
    pt = BlogPeriodicTasks()

    ctx = auth_ctx.MistralContext(
        user_id=None,
        project_id=None,
        auth_token=None,
        is_admin=True
    )

    tg.add_dynamic_timer(
        pt.run_periodic_tasks,
        initial_delay=None,
        periodic_interval_max=1,
        context=ctx
    )
