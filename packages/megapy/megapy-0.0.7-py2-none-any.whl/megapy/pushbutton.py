from arduino import ArduinoConnection, ArduinoObject

class PushButton(ArduinoObject):

    _lastPin = 1

    def __init__(self, conn, pin):
        ArduinoObject.__init__(self, conn, 'pb' + str(pin), 'pushbutton')
        super(PushButton, self).create(pin)

    def _get_state(self):
        return int(super(PushButton, self).get("state"))

    def _get_clicks(self):
        return int(super(PushButton, self).get("clicks"))

    def _get_pin(self):
        return int(super(PushButton, self).get("pin"))

    def enable(self):
        return super(PushButton, self).do("enable")

    def disable(self):
        return super(PushButton, self).do("disable")

    def reset(self):
        return super(PushButton, self).do("reset")

    state = property(_get_state)
    clicks = property(_get_clicks)
    pin = property(_get_pin)
