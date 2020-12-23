import magichue


class wifi_lamp:

    def __init__(self, ipaddr):
        self.light = magichue.Light(ipaddr)

    def alert(self, speed, color):
        self.light.speed = speed
        if self.light.is_white:
            self.light.is_white = False
            self.light.mode = color
        if not self.light.on:
            self.light.on = True

    def red_alert(self, speed=1.0):
        return self.alert(speed, magichue.RED_GRADUALLY)

    def green_alert(self, speed=1.0):
        return self.alert(speed, magichue.GREEN_GRADUALLY)

    def off(self):
        self.light.on = False
