import falcon
import json
from megapy import Stepper
from app import MegaRestApp, Exception400
import traceback


class StepperResource(object):
    steppers = {}

    def __init__(self, conn):
        self.connection = conn

    def on_get(self, req, resp, name = None, cmd = None, arg = None):
        try:
            print "Received {} {} request with params {}".format(req.method, req.path, req.params)
            if name is None:
                raise Exception400("A Stepper name must be provided")
            elif name not in StepperResource.steppers:
                raise Exception400("Stepper {} does not exist".format(name))
            if cmd is None:
                raise Exception400("A Stepper command must be provided")
            stpr = StepperResource.steppers[name]
            if cmd == 'rpm':
                if arg is not None:
                    stpr.rpm = arg
                value = stpr.rpm
            elif cmd == 'microsteps':
                if arg is not None:
                    stpr.microsteps = arg
                value = stpr.microsteps
            elif cmd == 'stepsperrev':
                if arg is not None:
                    stpr.stepsperrev = arg
                value = stpr.stepsperrev
            elif cmd == 'dir':
                value = stpr.dir
            elif cmd == 'stepsremaining':
                value = stpr.stepsremaining
            elif cmd == 'stop':
                value = stpr.stop()
            elif cmd == 'enable':
                value = stpr.enable()
            elif cmd == 'disable':
                value = stpr.disable()
            elif cmd == 'rotate':
                if arg is not None:
                    value = stpr.rotate(arg)
                else:
                    raise Exception400("Rotation value in degrees must be provided")
            elif cmd == 'step':
                if arg is not None:
                    value = stpr.step(arg)
                else:
                    raise Exception400("Number of steps must be provided")
            else:
                raise Exception400("Command {} is invalid".format(cmd))
            resp.status = falcon.HTTP_200
            resp.media = { "error" : None, cmd: value }
        except Exception400 as ex:
            resp.status = falcon.HTTP_400
            resp.media = { "error" : str(ex) }
        except Exception as ex:
            resp.status = falcon.HTTP_500
            resp.media = { "error" : str(ex), "trace": traceback.format_exc() }


    def on_post(self, req, resp):
        print "Received {} {} request with params {}".format(req.method, req.path, req.params)

        try:
            number = req.media.get("number")
            if number is None:
                raise Exception400("A stepper number must be provided")
            stpr = Stepper(self.connection, number)
            StepperResource.steppers[stpr.name] = stpr
            resp.status = falcon.HTTP_200
            resp.media = { "error" : None, "name" : stpr.name }
        except Exception400 as ex:
            resp.status = falcon.HTTP_400
            resp.media = { "error" : str(ex) }
        except Exception as ex:
            resp.status = falcon.HTTP_500
            resp.media = { "error" : str(ex), "trace": traceback.format_exc() }
