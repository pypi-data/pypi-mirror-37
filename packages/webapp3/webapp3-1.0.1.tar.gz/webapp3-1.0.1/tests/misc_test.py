# -*- coding: utf-8 -*-
# Copyright 2011 webapp3 AUTHORS.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import six

from tests.test_base import BaseTestCase
import webapp3
import webob
import webob.exc


class TestMiscellaneous(BaseTestCase):

    def test_abort(self):
        self.assertRaises(webob.exc.HTTPOk, webapp3.abort, 200)
        self.assertRaises(webob.exc.HTTPCreated, webapp3.abort, 201)
        self.assertRaises(webob.exc.HTTPAccepted, webapp3.abort, 202)
        self.assertRaises(
            webob.exc.HTTPNonAuthoritativeInformation, webapp3.abort, 203)
        self.assertRaises(webob.exc.HTTPNoContent, webapp3.abort, 204)
        self.assertRaises(webob.exc.HTTPResetContent, webapp3.abort, 205)
        self.assertRaises(webob.exc.HTTPPartialContent, webapp3.abort, 206)
        self.assertRaises(webob.exc.HTTPMultipleChoices, webapp3.abort, 300)
        self.assertRaises(webob.exc.HTTPMovedPermanently, webapp3.abort, 301)
        self.assertRaises(webob.exc.HTTPFound, webapp3.abort, 302)
        self.assertRaises(webob.exc.HTTPSeeOther, webapp3.abort, 303)
        self.assertRaises(webob.exc.HTTPNotModified, webapp3.abort, 304)
        self.assertRaises(webob.exc.HTTPUseProxy, webapp3.abort, 305)
        self.assertRaises(webob.exc.HTTPTemporaryRedirect, webapp3.abort, 307)
        self.assertRaises(webob.exc.HTTPClientError, webapp3.abort, 400)
        self.assertRaises(webob.exc.HTTPUnauthorized, webapp3.abort, 401)
        self.assertRaises(webob.exc.HTTPPaymentRequired, webapp3.abort, 402)
        self.assertRaises(webob.exc.HTTPForbidden, webapp3.abort, 403)
        self.assertRaises(webob.exc.HTTPNotFound, webapp3.abort, 404)
        self.assertRaises(webob.exc.HTTPMethodNotAllowed, webapp3.abort, 405)
        self.assertRaises(webob.exc.HTTPNotAcceptable, webapp3.abort, 406)
        self.assertRaises(
            webob.exc.HTTPProxyAuthenticationRequired, webapp3.abort, 407)
        self.assertRaises(webob.exc.HTTPRequestTimeout, webapp3.abort, 408)
        self.assertRaises(webob.exc.HTTPConflict, webapp3.abort, 409)
        self.assertRaises(webob.exc.HTTPGone, webapp3.abort, 410)
        self.assertRaises(webob.exc.HTTPLengthRequired, webapp3.abort, 411)
        self.assertRaises(
            webob.exc.HTTPPreconditionFailed, webapp3.abort, 412)
        self.assertRaises(
            webob.exc.HTTPRequestEntityTooLarge, webapp3.abort, 413)
        self.assertRaises(webob.exc.HTTPRequestURITooLong, webapp3.abort, 414)
        self.assertRaises(
            webob.exc.HTTPUnsupportedMediaType, webapp3.abort, 415)
        self.assertRaises(
            webob.exc.HTTPRequestRangeNotSatisfiable, webapp3.abort, 416)
        self.assertRaises(webob.exc.HTTPExpectationFailed, webapp3.abort, 417)
        self.assertRaises(
            webob.exc.HTTPInternalServerError, webapp3.abort, 500)
        self.assertRaises(webob.exc.HTTPNotImplemented, webapp3.abort, 501)
        self.assertRaises(webob.exc.HTTPBadGateway, webapp3.abort, 502)
        self.assertRaises(
            webob.exc.HTTPServiceUnavailable, webapp3.abort, 503)
        self.assertRaises(webob.exc.HTTPGatewayTimeout, webapp3.abort, 504)
        self.assertRaises(
            webob.exc.HTTPVersionNotSupported, webapp3.abort, 505)

        # Invalid use 500 as default.
        self.assertRaises(KeyError, webapp3.abort, 0)
        self.assertRaises(KeyError, webapp3.abort, 999999)
        self.assertRaises(KeyError, webapp3.abort, 'foo')

    def test_import_string(self):
        self.assertEqual(webapp3.import_string('webob.exc'), webob.exc)
        self.assertEqual(webapp3.import_string('webob'), webob)

        self.assertEqual(webapp3.import_string('asdfg', silent=True), None)
        self.assertEqual(
            webapp3.import_string('webob.asdfg', silent=True),
            None
        )

        self.assertRaises(
            webapp3.ImportStringError, webapp3.import_string, 'asdfg')
        self.assertRaises(
            webapp3.ImportStringError, webapp3.import_string, 'webob.asdfg')

    def test_to_utf8(self):
        res = webapp3._to_utf8('ábcdéf'.decode('utf-8')
                               if six.PY2 else 'ábcdéf')
        self.assertIsInstance(res, six.binary_type, True)

        res = webapp3._to_utf8('abcdef')
        self.assertIsInstance(res, six.binary_type, True)

    '''
    # removed to simplify the codebase.
    def test_to_unicode(self):
        res = webapp3.to_unicode(unicode('foo'))
        self.assertEqual(isinstance(res, unicode), True)

        res = webapp3.to_unicode('foo')
        self.assertEqual(isinstance(res, unicode), True)
    '''

    def test_http_status_message(self):
        self.assertEqual(
            webapp3.Response.http_status_message(404),
            'Not Found'
        )
        self.assertEqual(
            webapp3.Response.http_status_message(500),
            'Internal Server Error'
        )
        self.assertRaises(KeyError, webapp3.Response.http_status_message, 9999)

    def test_cached_property(self):
        count = [0]

        class Foo(object):
            @webapp3.cached_property
            def bar(self):
                count[0] += 1
                return count[0]

        self.assertTrue(isinstance(Foo.bar, webapp3.cached_property))

        foo = Foo()
        self.assertEqual(foo.bar, 1)
        self.assertEqual(foo.bar, 1)
        self.assertEqual(foo.bar, 1)

    def test_redirect(self):
        app = webapp3.WSGIApplication()
        req = webapp3.Request.blank('/')
        req.app = app
        app.set_globals(app=app, request=req)
        rsp = webapp3.redirect('http://www.google.com/', code=301, body='Weee')
        self.assertEqual(rsp.status_int, 301)
        self.assertEqual(rsp.body, b'Weee')
        self.assertEqual(rsp.headers.get('Location'), 'http://www.google.com/')

    def test_redirect_to(self):
        app = webapp3.WSGIApplication([
            webapp3.Route('/home', handler='', name='home'),
        ])
        req = webapp3.Request.blank('/')
        req.app = app
        app.set_globals(app=app, request=req)

        rsp = webapp3.redirect_to('home', _code=301, _body='Weee')
        self.assertEqual(rsp.status_int, 301)
        self.assertEqual(rsp.body, b'Weee')
        self.assertEqual(rsp.headers.get('Location'), 'http://localhost/home')


if __name__ == '__main__':
    unittest.main()
