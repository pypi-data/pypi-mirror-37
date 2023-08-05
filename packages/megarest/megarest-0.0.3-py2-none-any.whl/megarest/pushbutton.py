import falcon
import json
from megapy import PushButton
from app import MegaRestApp, Exception400
import traceback


class PushButtonResource(object):
    buttons = {}
    def __init__(self, conn):
        self.connection = conn

    def validate(self, req, resp, name, cmd):

        if cmd is None:
            raise Exception400("A Pushbutton command must be provided")

    def on_get(self, req, resp, name = None, cmd = None):
        try:
            print "Received {} {} request with params {}".format(req.method, req.path, req.params)
            if name is None:
                raise Exception400("A Pushbutton name must be provided")
            elif name not in PushButtonResource.buttons:
                raise Exception400("Pushbutton {} does not exist".format(name))
            pb = PushButtonResource.buttons[name]
            if cmd is None:
                cmd = 'state'
            if cmd == 'state':
                value = pb.state
            elif cmd == 'clicks':
                value = pb.clicks
            elif cmd == 'pin':
                value = pb.pin
            elif cmd == 'reset':
                value = pb.reset()
            elif cmd == 'enable':
                value = pb.enable()
            elif cmd == 'disable':
                value = pb.disable()
            else:
                raise Exception400("Command {} is invalid".format(cmd))
            resp.status = falcon.HTTP_200
            resp.media = { "error" : None, cmd : value }
        except Exception400 as ex:
            resp.status = falcon.HTTP_400
            resp.media = { "error" : str(ex) }
        except Exception as ex:
            resp.status = falcon.HTTP_500
            resp.media = { "error" : str(ex), "trace": traceback.format_exc() }


    def on_post(self, req, resp):
        print "Received {} {} request with params {}".format(req.method, req.path, req.params)

        try:
            pin = req.media.get("pin")
            if pin is None:
                raise Exception400("A PushButton pin number must be provided")
            pb = PushButton(self.connection, pin)
            PushButtonResource.buttons[pb.name] = pb
            resp.status = falcon.HTTP_200
            resp.media = { "error" : None, "name" : pb.name }
        except Exception400 as ex:
            resp.status = falcon.HTTP_400
            resp.media = { "error" : str(ex) }
        except Exception as ex:
            resp.status = falcon.HTTP_500
            resp.media = { "error" : str(ex), "trace": traceback.format_exc() }
