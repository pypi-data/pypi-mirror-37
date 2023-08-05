from __future__ import unicode_literals
from app import MegaRestApp
from api import MegaRestAPI

print "Starting Arduino Mega REST API Server"
options = {
    'bind': '%s:%s' % ('0.0.0.0', '8080'),
    'workers': 1,
    'timeout': 1000
}

MegaRestApp(MegaRestAPI(), options).run()
