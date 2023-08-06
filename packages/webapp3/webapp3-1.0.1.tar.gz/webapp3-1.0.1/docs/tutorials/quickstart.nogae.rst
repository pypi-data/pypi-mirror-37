.. _tutorials.quickstart.nogae:

Quick start (to use webapp3 outside of App Engine)
==================================================
webapp3 can also be used outside of App Engine as a general purpose web
framework, as it has these features:

- It is independent of the App Engine SDK. If the SDK is not found, it sets
  fallbacks to be used outside of App Engine.
- It supports threaded environments through the module :ref:`api.webapp3_extras.local`.
- All webapp3_extras modules are designed to be thread-safe.
- It is compatible with ``WebOb`` 1.0 and superior, which fixes several bugs
  found in the version bundled with the SDK (which is of course supported as
  well).

It won't support App Engine services, but if you like webapp, why not use it
in other servers as well? Here we'll describe how to do this.

.. note::
   If you want to use webapp3 on App Engine,
   read the :ref:`tutorials.quickstart` tutorial instead.


Prerequisites
-------------
If you don't have a package installer in your system yet (like ``pip`` or
``easy_install``), install one. See :ref:`tutorials.installing.packages`.

If you don't have ``virtualenv`` installed in your system yet, install it.
See :ref:`tutorials.virtualenv`.


Create a directory for your app
-------------------------------
Create a directory ``hellowebapp3`` for your new app. It is where you will
setup the environment and create your application.


Install WebOb, Paste and webapp3
--------------------------------
We need three libraries to use webapp3: `WebOb <http://pypi.python.org/pypi/WebOb>`_, for Request and Response objects,
`Paste <http://pypi.python.org/pypi/Paste>`_, for the development server,
and `webapp3 <http://pypi.python.org/pypi/webapp3>`_ itself.

Type this to install them using the **active virtual environment**
(see :ref:`tutorials.virtualenv`):

.. code-block:: text

   $ pip install WebOb
   $ pip install Paste
   $ pip install webapp3

Or, using easy_install:

.. code-block:: text

   $ easy_install WebOb
   $ easy_install Paste
   $ easy_install webapp3

Now the environment is ready for your first app.


Hello, webapp3!
---------------
Create a file ``main.py`` inside your ``hellowebapp3`` directory and define
a handler to display a 'Hello, webapp3!' message. This will be our bootstrap
file::

    import webapp3

    class HelloWebapp3(webapp3.RequestHandler):
        def get(self):
            self.response.write('Hello, webapp3!')

    app = webapp3.WSGIApplication([
        ('/', HelloWebapp3),
    ], debug=True)

    def main():
        from paste import httpserver
        httpserver.serve(app, host='127.0.0.1', port='8080')

    if __name__ == '__main__':
        main()


Test your app
-------------
Now start the development server using the Python executable provided by
virtualenv:

.. code-block:: text

   $ python main.py

The web server is now running, listening for requests on port 8080. You can
test the application by visiting the following URL in your web browser:

    http://127.0.0.1:8080/
