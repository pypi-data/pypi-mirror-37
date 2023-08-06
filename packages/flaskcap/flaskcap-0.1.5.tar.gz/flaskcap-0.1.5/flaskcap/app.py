# coding:utf-8

import sys
import time
import logging

from flask.app import Flask, setupmethod
from flask.blueprints import Blueprint
from flask.globals import g


def patch_blueprint():
    '''Patch blueprint for access log'''
    def _log_access(self, f):
        def _log(s):
            s.app.log_access_func = f

        self.record_once(_log)
        return f

    Blueprint.log_access = _log_access


patch_blueprint()


class FlaskCap(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskCap, self).__init__(*args, **kwargs)
        self.elapsed_time = None
        self.log_access_func = None
        self.access_logger = logging.getLogger('flaskcap.access')
        self.access_logger.setLevel(logging.INFO)
        self.error_logger = logging.getLogger('flaskcap.error')

    @setupmethod
    def log_access(self, f):
        """Register a function for logging access.

        Your function must take two parameters:
        an instance of :attr:`request_class` and an instance of :attr:`response_class`.

        e.g.
        @app.log_access
        def access_handler(request, response):
            app.logger.info('Handler a request in %ss' % app.elapsed_time)
        """
        self.log_access_func = f
        return f

    def wsgi_app(self, environ, start_response):
        """The actual WSGI application. This is not implemented in
        :meth:`__call__` so that middlewares can be applied without
        losing a reference to the app object. Instead of doing this::

            app = MyMiddleware(app)

        It's a better idea to do this instead::

            app.wsgi_app = MyMiddleware(app.wsgi_app)

        Then you still have the original application object around and
        can continue to call methods on it.

        .. versionchanged:: 0.7
            Teardown events for the request and app contexts are called
            even if an unhandled error occurs. Other events may not be
            called depending on when an error occurs during dispatch.
            See :ref:`callbacks-and-errors`.

        :param environ: A WSGI environment.
        :param start_response: A callable accepting a status code,
            a list of headers, and an optional exception context to
            start the response.
        """
        _start_time = time.time()
        ctx = self.request_context(environ)
        error = None
        try:
            try:
                ctx.push()
                if ctx.request.data:
                    if ctx.request.is_json:
                        g.request_payload = ctx.request.json
                    else:
                        g.request_payload = ctx.request.data
                else:
                    g.request_payload = ctx.request.values.to_dict()
                response = self.full_dispatch_request()
            except Exception as e:
                error = e
                response = self.handle_exception(e)
            except:
                error = sys.exc_info()[1]
                raise
            self.elapsed_time = round(time.time() - _start_time, 2)
            if self.log_access_func:
                self.log_access_func(ctx.request, response)
            return response(environ, start_response)
        finally:
            if self.should_ignore_error(error):
                error = None
            ctx.auto_pop(error)
