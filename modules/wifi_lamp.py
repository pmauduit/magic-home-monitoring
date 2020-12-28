import magichue


class wifi_lamp:

    def __init__(self, ipaddr):
        self._ipaddr = ipaddr
        self.light = magichue.Light(self._ipaddr)

    def _recycle(self):
        self.light = magichue.Light(self._ipaddr)

    def alert(self, speed, color):
        self._recycle()
        self.light.speed = speed
        self.light.is_white = False
        self.light.mode = color
        self.light.on = True

    def white(self, brightness=255):
        self._recycle()
        self.light.is_white = True
        self.light.brightness = brightness
        self.light.on = True


    def red_alert(self, speed=1.0):
        return self.alert(speed, magichue.RED_GRADUALLY)

    def green_alert(self, speed=1.0):
        return self.alert(speed, magichue.GREEN_GRADUALLY)

    def off(self):
        self._recycle()
        self.light.on = False
