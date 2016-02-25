1. Follow Devstack documentation to setup a host for Devstack. Then clone
   Devstack source code::

      $ git clone https://github.com/openstack-dev/devstack

1. Clone Blog source code::

      $ git clone https://github.com/stackforge/blog

1. Copy Blog integration scripts to Devstack::

      $ cp blog/contrib/devstack/lib/blog ${DEVSTACK_DIR}/lib
      $ cp blog/contrib/devstack/extras.d/70-blog.sh ${DEVSTACK_DIR}/extras.d/

1. Create/modify a ``localrc`` file as input to devstack::

      $ cd devstack
      $ touch localrc

1. The Blog service is not enabled by default, so it must be enabled in ``localrc``
   before running ``stack.sh``. This example of ``localrc``
   file shows all of the settings required for Blog::

      # Enable Blog
      enable_service blog

1. Deploy your OpenStack Cloud with Blog::

   $ ./stack.sh


Note: 
1. All needed Blog keystone endpoints will be automatically created
during installation.
1. Python-blogclient also will be automatically cloned and installed.
