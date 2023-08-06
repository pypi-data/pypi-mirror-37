from __future__ import unicode_literals
from gunicorn.app.base import BaseApplication
from gunicorn.six import iteritems


class Exception400(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class MegaRestApp(BaseApplication):
    connection = None

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(MegaRestApp, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
