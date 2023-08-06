import webapp3


class LazyHandler(webapp3.RequestHandler):
    def get(self, **kwargs):
        self.response.out.write('I am a laaazy view.')


class CustomMethodHandler(webapp3.RequestHandler):
    def custom_method(self):
        self.response.out.write('I am a custom method.')


def handle_exception(request, response, exception):
    return webapp3.Response(body='Hello, custom response world!')
