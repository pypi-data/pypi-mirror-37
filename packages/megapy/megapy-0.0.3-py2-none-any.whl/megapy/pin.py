from arduino import ArduinoConnection, ArduinoObject
import time

class DigitalPin(ArduinoObject):

    _lastPin = 1

    def __init__(self, conn, pin, mode='input'):
        ArduinoObject.__init__(self, conn, 'dp' + str(DigitalPin._lastPin), 'pin digial')
        self.pin = pin
        self.mode = mode
        super(DigitalPin, self).create("{} {}".format(self.mode, self.pin))
        DigitalPin._lastPin += 1

    def _get_value(self):
        return int(super(DigitalPin, self).get("value"))

    def _set_value(self, value):
        return super(DigitalPin, self).set("value", value)

    value = property(_get_value, _set_value)

class AnalogPin(ArduinoObject):

    _lastPin = 1

    def __init__(self, conn, pin):
        ArduinoObject.__init__(self, conn, 'ap' + str(AnalogPin._lastPin), 'pin analog')
        self.pin = pin
        super(AnalogPin, self).create("input {}".format(self.pin))
        AnalogPin._lastPin += 1

    def _get_value(self):
        return int(super(AnalogPin, self).get("value"))

    value = property(_get_value)
