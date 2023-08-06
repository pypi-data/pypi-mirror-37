.. _tutorials.quickstart:

Quick start
===========
If you already know `webapp <http://code.google.com/appengine/docs/python/tools/webapp/>`_,
webapp3 is very easy to get started. You can use webapp3 exactly like webapp,
and learn the new features as you go.

If you are new to App Engine, read :ref:`tutorials.gettingstarted.index` first.
You will need the `App Engine SDK <https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python>`_
installed for this quick start.

.. note::
   If you want to use webapp3 outside of App Engine,
   read the :ref:`tutorials.quickstart.nogae` tutorial instead.


Create an application
---------------------
Create a directory ``hellowebapp3`` for your new app.
`Download webapp3 <http://code.google.com/p/webapp-improved/downloads/list>`_,
unpack it and add ``webapp3.py`` to that directory. If you want to use extra
features such as sessions, extra routes, localization, internationalization
and more, also add the ``webapp3_extras`` directory to your app.

.. note::
   webapp3 is part of the Python 2.7 runtime since App Engine SDK 1.6.0,
   so you don't need to upload it with your app anymore. To include it in
   your app see
   `Configuring Libraries <https://cloud.google.com/appengine/docs/python/tools/libraries27>`_.

Hello, webapp3!
---------------
Create an ``app.yaml`` file in your app directory with the following contents:

.. code-block:: yaml

   application: helloworld
   version: 1
   runtime: python27
   api_version: 1
   threadsafe: true

   handlers:
   - url: /.*
     script: main.app

Then create a file ``main.py`` and define a handler to display a
'Hello, webapp3!' message::

    import webapp3

    class HelloWebapp3(webapp3.RequestHandler):
        def get(self):
            self.response.write('Hello, webapp3!')

    app = webapp3.WSGIApplication([
        ('/', HelloWebapp3),
    ], debug=True)


Test your app
-------------
If you're using the Google App Engine Launcher, you can set up the application
by selecting the **File** menu, **Add Existing Application...**, then selecting
the ``hellowebapp3`` directory. Select the application in the app list, click
the Run button to start the application, then click the Browse button to view
it. Clicking Browse simply loads (or reloads)
`http://localhost:8080/ <http://localhost:8080/>`_ in your default web browser.

If you're not using Google App Engine Launcher, start the web server with the
following command, giving it the path to the ``hellowebapp3`` directory:

.. code-block:: text

   google_appengine/dev_appserver.py helloworld/

The web server is now running, listening for requests on port 8080. You can
test the application by visiting the following URL in your web browser:

    http://localhost:8080/
