import falcon
import json
from megapy import DigitalPin, AnalogPin, MegaException
from app import MegaRestApp, Exception400
import traceback


class PinResource(object):
    pins = {}

    def __init__(self, conn):
        self.connection = conn

    def on_get(self, req, resp, name = None, cmd = None, arg = None):
        try:
            print "Received {} {} request with params {}".format(req.method, req.path, req.params)
            if name is None:
                raise Exception400("A pin name must be provided")
            elif name not in PinResource.pins:
                raise Exception400("Pin {} does not exist".format(name))

            pin = PinResource.pins[name]
            if arg is not None and pin.__class__ == AnalogPin:
                raise Exception400("Cannot set value for an analog pin")

            if cmd is None:
                cmd = 'value'
            if cmd == 'value':
                if arg is not None:
                    pin.value = arg
                value = pin.value
            elif cmd == 'pin':
                value = pin.pin
            elif cmd == 'mode':
                value = pin.mode
            else:
                raise Exception400("Command {} is invalid".format(cmd))
            resp.status = falcon.HTTP_200
            resp.media = { "error" : None, cmd : value }
        except Exception400 as ex:
            resp.status = falcon.HTTP_400
            resp.media = { "error" : str(ex) }
        except MegaException as ex:
            resp.status = falcon.HTTP_404
            resp.media = { "error" : str(ex) }
        except Exception as ex:
            resp.status = falcon.HTTP_500
            resp.media = { "error" : str(ex), "trace": traceback.format_exc() }


    def on_post(self, req, resp):
        print "Received {} {} request with params {}".format(req.method, req.path, req.params)

        try:
            type = req.media.get("type")
            pin = req.media.get("pin")
            mode = req.media.get("mode")
            thePin = None
            if pin is None:
                raise Exception400("A pin number must be provided")
            if type == "digital":
                if mode is None or mode not in [ "input", "output" ]:
                    raise Exception400("A mode ('input' | 'output') must be provided")
                thePin = DigitalPin(self.connection, pin, mode)
            elif type == "analog":
                thePin = AnalogPin(self.connection, pin)
            else:
                raise Exception400("Invalid type of pin: {}".format(type))
            PinResource.pins[thePin.name] = thePin
            resp.status = falcon.HTTP_200
            resp.media = { "error" : None, "name" : thePin.name }
        except Exception400 as ex:
            resp.status = falcon.HTTP_400
            resp.media = { "error" : str(ex) }
        except MegaException as ex:
            resp.status = falcon.HTTP_404
            resp.media = { "error" : str(ex) }
        except Exception as ex:
            resp.status = falcon.HTTP_500
            resp.media = { "error" : str(ex), "trace": traceback.format_exc() }
