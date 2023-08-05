from arduino import ArduinoConnection, ArduinoObject

class DigitalPin(ArduinoObject):

    def __init__(self, conn, pin, mode='input'):
        ArduinoObject.__init__(self, conn, 'dp'  + str(pin), 'pin digital')
        self._pin = pin
        self._mode = mode
        super(DigitalPin, self).create("{} {}".format(mode, pin))

    def _get_value(self):
        return int(super(DigitalPin, self).get("value"))

    def _set_value(self, value):
        return super(DigitalPin, self).set("value", value)

    def _get_pin(self):
        return self._pin

    def _get_mode(self):
        return self._mode

    value = property(_get_value, _set_value)
    pin = property(_get_pin)
    mode = property(_get_mode)

class AnalogPin(ArduinoObject):

    def __init__(self, conn, pin):
        ArduinoObject.__init__(self, conn, 'ap' + str(pin), 'pin analog')
        self._pin = pin
        super(AnalogPin, self).create("input {}".format(pin))

    def _get_value(self):
        return int(super(AnalogPin, self).get("value"))

    def _get_pin(self):
        return self._pin

    value = property(_get_value)
    pin = property(_get_pin)
