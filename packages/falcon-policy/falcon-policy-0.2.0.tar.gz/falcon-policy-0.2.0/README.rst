Falcon Middleware: Policy Middleware |Build Status| |codecov.io|
================================================================

The ``falcon-policy`` package provides a middleware component
that enables simple policy controls such as role-based access on routes
via configuration.

The configuration approach to policy rules enables dynamic authorization
use-cases where the policy needs to be adjusted on-demand without a new
service deployment.

Installation
------------

.. code:: bash

    $ pip install falcon-policy

Usage
-----

The ``RoleBasedPolicy`` middleware class examines each incoming request
and verifies the ``roles`` list from the request context; which should be
populated by an authentication middleware. If the request context isn't
populated with a ``roles`` list, then the middleware will fall back on
the ``X-Roles`` header for the appropriate role given the request being made.
Usage of the ``X-Roles`` header, is primarily used when handling
authentication outside of the middleware stack or for development with
authentication disabled.

Implementation Note:

If the request context type isn't a dictionary, the middleware will assume
that ``req.context`` is an Object with a ``roles`` attribute.


Getting Started:

* Create a policy configuration
* Create an instance of ``RoleBasedPolicy`` using the configuration
* Pass the instance to the ``falcon.API()`` initializer:

.. code:: python

    from falcon_policy import RoleBasedPolicy

    policy_config = {
        'roles': [
            'admin',
            'creator',
            'observer',
        ],
        'groups': {
            'create': ['admin', 'creator'],
            'update': ['admin', 'creator'],
            'read': ['admin', 'creator', 'observer'],
            'delete': ['admin'],
        },
        'routes': {
            '/quote': {
                'GET': ['read'],
                'POST': ['create'],
                'PUT': ['update'],
                'DELETE': ['delete'],
            },
            '/quote/{id}': {
                'GET': ['read'],
                'POST': ['create'],
                'PUT': ['update'],
                'DELETE': ['delete'],
            },
            '/status': {
                'GET': ['@any-role'],
                'HEAD': ['@passthrough'],
            },
        },
    }

    app = falcon.API(
        middleware=[
            RoleBasedPolicy(policy_config)
        ]
    )


If validation fails an instance of ``falcon.HTTPForbidden`` is raised.

Configuration
-------------

The policy configuration is separated into three sections:

* Roles: Is a list of names that correspond with Role values provided
  by your authentication system.
* Groups: Is an alias/grouping of multiple role names for convenience.
* Routes: A structure containing role and/or group permissions for a given
  Falcon route and method.

Specialty Roles:

    ``falcon-policy`` offers two specialty roles types that should be used with
    care:

    * ``@any-role``: Allows any defined role
    * ``@passthrough``: Allows all users (authenticated and unauthenticated)


About Falcon
------------

Falcon is a `bare-metal Python web
framework <http://falconframework.org/index.html>`__ for building lean and
mean cloud APIs and app backends. It encourages the REST architectural style,
and tries to do as little as possible while remaining `highly
effective <http://falconframework.org/index.html#Benefits>`__.


.. |Build Status| image:: https://travis-ci.org/falconry/falcon-policy.svg
   :target: https://travis-ci.org/falconry/falcon-policy
.. |codecov.io| image:: https://codecov.io/gh/falconry/falcon-policy/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/falconry/falcon-policy
