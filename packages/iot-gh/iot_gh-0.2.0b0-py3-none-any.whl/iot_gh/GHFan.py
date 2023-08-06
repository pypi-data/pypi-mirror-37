import pigpio

class GHFan(object):
    """This class GHFan provides a services to control the IoT Greenhouse fan
    """
    
    FAN_ON = True
    FAN_OFF = False

    _pi = None
    _gpio = 0
        
    def __init__(self, pi, fan_gpio):
        """Constructor for class GHFan
        
        :param pi: reference to pigpio service
        :param fan_gpio: GPIO port for fan. Use GHgpio definitions.
        :returns: GHFan object
        """
        self._pi = pi
        self._gpio = fan_gpio
            
        self._pi.set_mode(self._gpio, pigpio.OUTPUT)        
        #Fan off
        self._pi.write(self._gpio, self.FAN_OFF)
        
    def on(self):
        self._pi.write(self._gpio, self.FAN_ON)
        
    def off(self):
        self._pi.write(self._gpio, self.FAN_OFF)
        
    def get_state(self):
        return self._pi.read(self._gpio)

    def is_on(self):
        return self.get_state() == self.FAN_ON

    def is_off(self):
        return self.get_state() == self.FAN_OFF
