from time import sleep
import pigpio

class GHSwitches(object):
    """This class GHSwtiches provides a services to control the both IoT Greenhouse switches
    """

    SWITCH_ON = False
    SWITCH_OFF = True
    
    push_button = None
    toggle = None
    
    def __init__(self, pi, pb_switch_gpio, toggle_switch_gpio):
        """Constructor for class GHSwitches
    
        Returns references to both push button and toggle switches

        :param pi: reference to pigpio service
        :param pb_switch_gpio: GPIO port for push button switch. Use GHgpio definitions.
        :param toggle_switch_gpio: GPIO port for toggle switch. Use GHgpio definitions.
        :returns: GHSwitches object
        """
        self.push_button = GHSwitch(pi, pb_switch_gpio)
        self.toggle = GHSwitch(pi, toggle_switch_gpio)

class GHSwitch(object):
    """This class GHSwtiches provides a services to an IoT Greenhouse switch
    """
        
    _pi = None
    _gpio = 0
    
    def __init__(self, pi, switch_gpio):
        """Constructor for class GHSwitch
        
        Returns references to switch object. Used for both push button and toggle.

        :param pi: reference to pigpio service
        :param switch_gpio: GPIO port for switch. Use GHgpio definitions.
        :returns: GHSwitch object
        """
        self._pi = pi
        self._gpio = switch_gpio
        self._pi.set_mode(self._gpio, pigpio.INPUT)        
        
    def get_state(self):
        #debounce
        first_read = False
        second_read = True
        debouce_delay = .01
        while first_read != second_read:
            first_read = self._pi.read(self._gpio)
            sleep(debouce_delay)
            second_read = self._pi.read(self._gpio)
        return first_read

    def wait_for_press(self):
        #Wait for on - active low
        while self.get_state():
            sleep(.5)

    def wait_for_release(self):
        #Wait for off - active low
        while not self.get_state():
            sleep(.5)

    def wait_for_press_and_release(self):
        self.wait_for_press()
        self.wait_for_release()
