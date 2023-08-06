from time import sleep
import pigpio

class GHBuzzer(object):
    """This class GHBuzzer provides a services to control the IoT Greenhouse buzzer.
    """
    BUZZER_ON = False
    BUZZER_OFF = True
    BEEP_DELAY_ON = .5
    BEEP_DELAY_OFF = .3

    _pi = None
    _gpio = 0
    
    def __init__(self, pi, buzzer_gpio):
        """Constructor for class GHBuzzer
        
        :param pi: reference to pigpio service
        :param buzzer_gpio: GPIO port for buzzer. Use GHgpio definitions.
        :returns: GHBuzzer object
        """
        self._pi = pi
        self._gpio = buzzer_gpio

        self._pi.set_mode(self._gpio, pigpio.OUTPUT)        
        #buzzer off
        self._pi.write(self._gpio, self.BUZZER_OFF)
        
    def on(self):
        self._pi.write(self._gpio, self.BUZZER_ON)

    def off(self):
        self._pi.write(self._gpio, self.BUZZER_OFF)

    def beep(self, delay = BEEP_DELAY_ON):
        self.on()
        sleep(delay)
        self.off()
 
    def beeps(self, delay = BEEP_DELAY_ON, beep_count = 2):
        for i in range(0, beep_count):
            if i > 0:
                sleep(self.BEEP_DELAY_OFF)
        self.beep(delay)
            
    def get_state(self):
        return self._pi.read(self._gpio)

    def is_on(self):
        return self.get_state() == self.BUZZER_ON

    def is_off(self):
        return self.get_state() == self.BUZZER_OFF

