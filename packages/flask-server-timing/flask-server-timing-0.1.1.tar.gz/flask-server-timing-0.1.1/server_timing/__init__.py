import logging
import flask
import datetime

from flask import request

from contextlib import contextmanager
from functools import partial, wraps

log = logging.getLogger()


class Timing():
    debug = False

    def __init__(self, app, force_debug=False):
        if app.debug or force_debug:
            Timing.debug = True
            log.info("Setting up after-request handler to add server timing header")
            app.after_request(Timing._add_header)

    @staticmethod
    def start(key):
        if not flask.has_request_context():
            log.debug("No request context available - start timing ignored")
            return

        if not hasattr(request, 'context'):
            request.context = {}

        request.context[key.replace(' ', '-')] = {'start': datetime.datetime.now()}

    @staticmethod
    def stop(key):
        if not flask.has_request_context() or not hasattr(request, 'context'):
            log.debug("No request context available - stop timing ignored")
            return

        _key = key.replace(' ', '-')
        if not _key in request.context:
            log.warn("Key '{}' not found in request context".format(key))
            return

        stop_time = datetime.datetime.now()
        start_time = request.context.get(_key, {}).get('start')
        if start_time:
            request.context[_key] = (stop_time - start_time).total_seconds() * 1000
        else:
            log.warn("No start time found for key '{}'".format(key))

    @staticmethod
    @contextmanager
    def time(key):
        Timing.start(key)
        yield key
        Timing.stop(key)

    @staticmethod
    def timer(f=None, name=None):
        if f is None:
            return partial(Timing.timer, name=name)

        if not Timing.debug:
            log.debug("Mode is not set to 'debug' - not wrapping function for timing")
            return f

        @wraps(f)
        def wrapper(*args, **kwds):
            with Timing.time(name or f.__name__):
                return f(*args, **kwds)

        return wrapper

    @staticmethod
    def _add_header(response):
        if flask.has_request_context() and flask.request.context:
            timing_list = [key + ';dur=' + str(val) + ';desc="' + key + '"' for key, val in flask.request.context.items()]
            response.headers.set('Server-Timing', ', '.join(timing_list))

        return response
