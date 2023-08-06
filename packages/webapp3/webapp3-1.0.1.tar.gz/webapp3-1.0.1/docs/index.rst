.. _index:

.. webapp3 documentation master file, created by
   sphinx-quickstart on Sat Jul 31 10:41:37 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to webapp3!
===================
`webapp3`_ is a lightweight Python web framework compatible with Google App
Engine's `webapp`_.

webapp3 is a `simple`_. it follows the simplicity of webapp, but improves
it in some ways: it adds better URI routing and exception handling, a full
featured response object and a more flexible dispatching mechanism.

webapp3 also offers the package :ref:`webapp3_extras <index.api-reference-webapp3-extras>`
with several optional utilities: sessions, localization, internationalization,
domain and subdomain routing, secure cookies and others.

webapp3 can also be used outside of Google App Engine, independently of the
App Engine SDK.

For a complete description of how webapp3 improves webapp, see :ref:`features`.

.. note::
   webapp3 is part of the Python 2.7 runtime since App Engine SDK 1.6.0.
   To include it in your app see
   `Configuring Libraries <https://cloud.google.com/appengine/docs/python/tools/libraries27>`_.


Quick links
-----------
- `Package Index Page <https://pypi.python.org/pypi/webapp3>`_
- `Github <https://github.com/GoogleCloudPlatform/webapp3>`_
- `Discussion Group <https://groups.google.com/forum/#!forum/google-appengine>`_

Status
------

Webapp3 is currently maintained by Google Cloud Platform Developer Relations. It
is not an official Google product, but is hosted by Google to allow the webapp3
community to continue to maintain the project.

Tutorials
---------
.. toctree::
   :maxdepth: 1

   tutorials/quickstart.rst
   tutorials/quickstart.nogae.rst
   tutorials/gettingstarted/index.rst
   tutorials/i18n.rst


Guide
-----
.. toctree::
   :maxdepth: 3

   guide/app.rst
   guide/routing.rst
   guide/handlers.rst
   guide/request.rst
   guide/response.rst
   guide/exceptions.rst
   guide/testing.rst
   guide/extras.rst


API Reference - webapp3
-----------------------
.. toctree::
   :maxdepth: 2

   api/webapp3.rst


.. _index.api-reference-webapp3-extras:

API Reference - webapp3_extras
------------------------------
.. toctree::
   :maxdepth: 1

   api/webapp3_extras/auth.rst
   api/webapp3_extras/i18n.rst
   api/webapp3_extras/jinja2.rst
   api/webapp3_extras/json.rst
   api/webapp3_extras/local.rst
   api/webapp3_extras/mako.rst
   api/webapp3_extras/routes.rst
   api/webapp3_extras/securecookie.rst
   api/webapp3_extras/security.rst
   api/webapp3_extras/sessions.rst


API Reference - webapp3_extras.appengine
----------------------------------------
Modules that use App Engine libraries and services are restricted to
``webapp3_extras.appengine``.

.. toctree::
   :maxdepth: 1

   api/webapp3_extras/appengine/sessions_memcache.rst
   api/webapp3_extras/appengine/sessions_ndb.rst
   api/webapp3_extras/appengine/auth/models.rst
   api/webapp3_extras/appengine/users.rst


Miscelaneous
------------
.. toctree::
   :maxdepth: 1

   features.rst


Indices and tables
------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. Old docs linking to new ones or pages we don't want to link.

.. toctree::
   :hidden:

   api/index.rst
   api/extras.config.rst
   api/extras.i18n.rst
   api/extras.jinja2.rst
   api/extras.json.rst
   api/extras.local.rst
   api/extras.local_app.rst
   api/extras.mako.rst
   api/extras.routes.rst
   api/extras.securecookie.rst
   api/extras.security.rst
   api/extras.sessions.rst
   api/extras.sessions_memcache.rst
   api/extras.sessions_ndb.rst
   api/extras.users.rst
   guide/index.rst
   tutorials/index.rst
   todo.rst


Requirements
------------
webapp3 is compatible with Python 2.5 and superior. No Python 3 yet.

`WebOb`_ is the only library required for the core functionality.

Modules from webapp3_extras may require additional libraries, as indicated in
their docs.


Credits
-------
webapp3 is a superset of `webapp`_, created by the App Engine team.

Because webapp3 is intended to be compatible with webapp, the official webapp
documentation is valid for webapp3 too. Parts of this documentation were ported
from the `App Engine documentation`_, written by the App Engine team and
licensed under the Creative Commons Attribution 3.0 License.

webapp3 has code ported from `Werkzeug`_ and `Tipfy`_.

webapp3_extras has code ported from Werkzeug, Tipfy and `Tornado Web Server`_.

The `Sphinx`_ theme mimics the App Engine documentation.


Contribute
----------
webapp3 is considered stable, feature complete and well tested, but if you
think something is missing or is not working well, please describe it in our
issue tracker:

    https://github.com/GoogleCloudPlatform/webapp3/issues

Let us know if you found a bug or if something can be improved. New tutorials
and webapp3_extras modules are also welcome, and tests or documentation are
never too much.

Thanks!


License
-------
webapp3 is licensed under the `Apache License 2.0`_.


.. _webapp: http://code.google.com/appengine/docs/python/tools/webapp/
.. _webapp3: https://github.com/GoogleCloudPlatform/webapp3
.. _simple: https://github.com/GoogleCloudPlatform/webapp3/blob/master/webapp3.py
.. _WebOb: http://docs.webob.org/
.. _Werkzeug: http://werkzeug.pocoo.org/
.. _Tipfy: http://www.tipfy.org/
.. _Tornado Web Server: http://www.tornadoweb.org/
.. _Sphinx: http://sphinx.pocoo.org/
.. _App Engine documentation: http://cloud.google.com/appengine/docs/
.. _Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0
