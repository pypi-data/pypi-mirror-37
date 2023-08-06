from arduino import ArduinoConnection, ArduinoObject

class Stepper(ArduinoObject):

    _lastPin = 1

    def __init__(self, conn, number):
        ArduinoObject.__init__(self, conn, 'stpr' + str(number), 'stepper')
        self.number = number
        super(Stepper, self).create(self.number)

    def _get_rpm(self):
        return int(super(Stepper, self).get("rpm"))

    def _set_rpm(self, value):
        return super(Stepper, self).set("rpm", value)

    def _get_microsteps(self):
        return int(super(Stepper, self).get("microsteps"))

    def _set_microsteps(self, value):
        return super(Stepper, self).set("microsteps", value)

    def _get_dir(self):
        return int(super(Stepper, self).get("dir"))

    def _get_stepsperrev(self):
        return int(super(Stepper, self).get("stepsperrev"))

    def _set_stepsperrev(self, value):
        return super(Stepper, self).set("stepsperrev", value)

    def _get_stepsremaining(self):
        return int(super(Stepper, self).get("stepsremaining"))

    def rotate(self, degrees):
        return super(Stepper, self).do("rotate " + str(degrees))

    def step(self, steps):
        return super(Stepper, self).do("step " + str(steps))

    def enable(self):
        return super(Stepper, self).do("enable")

    def disable(self):
        return super(Stepper, self).do("disable")

    def stop(self):
        return super(Stepper, self).do("stop")

    rpm = property(_get_rpm, _set_rpm)
    microsteps = property(_get_microsteps, _set_microsteps)
    stepsperrev = property(_get_stepsperrev, _set_stepsperrev)
    dir = property(_get_dir)
    stepsremaining = property(_get_stepsremaining)
