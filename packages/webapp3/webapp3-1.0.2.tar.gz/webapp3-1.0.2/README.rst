webapp3
=======

|Build Status| |Coverage Status| |PyPI Version|

`webapp3`_ is a lightweight Python web framework compatible with Google App
Engine's `webapp`_.

webapp3 is simple. it follows the simplicity of webapp, but
improves it in some ways: it adds better URI routing and exception handling,
a full featured response object and a more flexible dispatching mechanism.

webapp3 also offers the package `webapp3_extras`_ with several optional
utilities: sessions, localization, internationalization, domain and subdomain
routing, secure cookies and others.

webapp3 can also be used outside of Google App Engine, independently of the
App Engine SDK.

For a complete description of how webapp3 improves webapp, see
`webapp3 features`_.

Quick links
-----------

- `User Guide <https://webapp3.readthedocs.org/>`_
- `Repository <https://github.com/GoogleCloudPlatform/webapp3>`_
- `Discussion Group <https://groups.google.com/forum/#!forum/google-appengine>`_

.. _webapp: http://code.google.com/appengine/docs/python/tools/webapp/
.. _webapp3: https://github.com/GoogleCloudPlatform/webapp3
.. _webapp3_extras: https://webapp3.readthedocs.org/#api-reference-webapp3-extras
.. _webapp3 features: https://webapp3.readthedocs.org/features.html

Status
------

Webapp3 is currently maintained by Google Cloud Platform Developer Relations. It
is not an official Google product, but is hosted by Google to allow the webapp3
community to continue to maintain the project.

Contributing changes
--------------------

-  See `CONTRIBUTING.md`_

Licensing
---------

- Apache 2.0 - See `LICENSE`_

.. _LICENSE: https://github.com/GoogleCloudPlatform/webapp3/blob/master/LICENSE
.. _CONTRIBUTING.md: https://github.com/GoogleCloudPlatform/webapp3/blob/master/CONTRIBUTING.md
.. |Build Status| image:: https://travis-ci.org/GoogleCloudPlatform/webapp3.svg
   :target: https://travis-ci.org/GoogleCloudPlatform/webapp3
.. |Coverage Status| image:: https://codecov.io/github/GoogleCloudPlatform/webapp3/coverage.svg?branch=master
   :target: https://codecov.io/github/GoogleCloudPlatform/webapp3?branch=master
.. |PyPI Version| image:: https://img.shields.io/pypi/v/webapp3.svg
   :target: https://pypi.python.org/pypi/webapp3
