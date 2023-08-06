import falcon
import json
from megapy import ArduinoConnection, MegaException
from app import MegaRestApp, Exception400
import traceback


class DeviceResource(object):

    def __init__(self, conn):
        self.connection = conn

    def on_get(self, req, resp):
        try:
            print "Received {} {} request with params {}".format(req.method, req.path, req.params)
            ttys = self.connection.get_ttys()
            devices = []
            for t in ttys:
                d = {}
                for attr in [ "name", "description", "manufacturer", "device" ]:
                    d[attr] = getattr(t, attr)
                devices.append(d)
            resp.status = falcon.HTTP_200
            resp.media = { "error" : None, "devices" : devices }
        except Exception as ex:
            resp.status = falcon.HTTP_500
            resp.media = { "error" : str(ex), "trace": traceback.format_exc() }


    def on_post(self, req, resp):
        print "Received {} {} request with params {}".format(req.method, req.path, req.params)

        try:
            device = req.media.get("device")
            self.connection.open(device)
            resp.status = falcon.HTTP_200
            resp.media = { "error" : None }
        except MegaException as ex:
            resp.status = falcon.HTTP_404
            resp.media = { "error" : str(ex) }
        except Exception as ex:
            resp.status = falcon.HTTP_500
            resp.media = { "error" : str(ex), "trace": traceback.format_exc() }
