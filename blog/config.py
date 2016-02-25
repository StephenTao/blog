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

"""
Configuration options registration and useful routines.
"""

from oslo.config import cfg

from blog.openstack.common import log
from blog import version


launch_opt = cfg.ListOpt(
    'server',
    default=['all'],
    help='Specifies which blog server to start by the launch script. '
         'Valid options are all or any combination of '
         'api, engine, and executor.'
)

api_opts = [
    cfg.StrOpt('host', default='0.0.0.0', help='Blog API server host'),
    cfg.IntOpt('port', default=8989, help='Blog API server port')
]

pecan_opts = [
    cfg.StrOpt('root', default='blog.api.controllers.root.RootController',
               help='Pecan root controller'),
    cfg.ListOpt('modules', default=["blog.api"],
                help='A list of modules where pecan will search for '
                     'applications.'),
    cfg.BoolOpt('debug', default=False,
                help='Enables the ability to display tracebacks in the '
                     'browser and interactively debug during '
                     'development.'),
    cfg.BoolOpt('auth_enable', default=True,
                help='Enables user authentication in pecan.')
]

use_debugger = cfg.BoolOpt(
    "use-debugger",
    default=False,
    help='Enables debugger. Note that using this option changes how the '
    'eventlet library is used to support async IO. This could result '
    'in failures that do not occur under normal operation. '
    'Use at your own risk.'
)

engine_opts = [
    cfg.StrOpt('engine', default='default',
               help='log engine plugin'),
    cfg.StrOpt('host', default='0.0.0.0',
               help='Name of the engine node. This can be an opaque '
                    'identifier. It is not necessarily a hostname, '
                    'FQDN, or IP address.'),
    cfg.StrOpt('topic', default='engine',
               help='The message topic that the engine listens on.'),
    cfg.StrOpt('version', default='1.0',
               help='The version of the engine.')
]

executor_opts = [
    cfg.StrOpt('host', default='0.0.0.0',
               help='Name of the executor node. This can be an opaque '
                    'identifier. It is not necessarily a hostname, '
                    'FQDN, or IP address.'),
    cfg.StrOpt('topic', default='executor',
               help='The message topic that the executor listens on.'),
    cfg.StrOpt('version', default='1.0',
               help='The version of the executor.')
]

wf_trace_log_name_opt = cfg.StrOpt(
    'workflow_trace_log_name',
    default='workflow_trace',
    help='Logger name for pretty '
    'workflow trace output.'
)

CONF = cfg.CONF

CONF.register_opts(api_opts, group='api')
CONF.register_opts(engine_opts, group='engine')
CONF.register_opts(pecan_opts, group='pecan')
CONF.register_opts(executor_opts, group='executor')
CONF.register_opt(wf_trace_log_name_opt)

CONF.register_cli_opt(use_debugger)
CONF.register_cli_opt(launch_opt)

CONF.import_opt('verbose', 'blog.openstack.common.log')
CONF.set_default('verbose', True)
CONF.import_opt('debug', 'blog.openstack.common.log')
CONF.import_opt('log_dir', 'blog.openstack.common.log')
CONF.import_opt('log_file', 'blog.openstack.common.log')
CONF.import_opt('log_config_append', 'blog.openstack.common.log')
CONF.import_opt('log_format', 'blog.openstack.common.log')
CONF.import_opt('log_date_format', 'blog.openstack.common.log')
CONF.import_opt('use_syslog', 'blog.openstack.common.log')
CONF.import_opt('syslog_log_facility', 'blog.openstack.common.log')

# Extend oslo default_log_levels to include some that are useful for blog
# some are in oslo logging already, this is just making sure it stays this
# way.
default_log_levels = cfg.CONF.default_log_levels

logs_to_quieten = [
    'sqlalchemy=WARN',
    'oslo.messaging=INFO',
    'iso8601=INFO',
    'eventlet.wsgi.server=INFO',
    'stevedore=INFO',
    'blog.openstack.common.loopingcall=INFO',
    'blog.openstack.common.periodic_task=INFO',
    'blog.services.periodic=INFO'
]

for chatty in logs_to_quieten:
    if chatty not in default_log_levels:
        default_log_levels.append(chatty)

cfg.set_defaults(
    log.log_opts,
    default_log_levels=default_log_levels
)


def parse_args(args=None, usage=None, default_config_files=None):
    CONF(
        args=args,
        project='blog',
        version=version,
        usage=usage,
        default_config_files=default_config_files
    )
