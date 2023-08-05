import datetime
import pigpio
import configparser, os

from iot_gh.GHgpio import GHgpio
from iot_gh.GHAnalogService import GHAnalogService
from iot_gh.GHBuzzer import GHBuzzer
from iot_gh.GHFan import GHFan
from iot_gh.GHLamps import GHLamps
from iot_gh.GHServo import GHServo
from iot_gh.GHSwitches import GHSwitches
from iot_gh.GHTemperature import GHTemperature
from iot_gh.GHWebService import GHWebService
from iot_gh.IoTGreenhouse import IoTGreenhouse


class IoTGreenhouseService(object):
    """IoT Greenhouse service class for IoT Greenhouse
    
    Provides references to input and output objects.
    """
    _pi = None      #pigpio connection
    _url = None
    _servo_ccw_limit = None
    _servo_cw_limit = None
    
    version = None
    
    analog_service = None
    ain_pot = None
    ain_temp = None
    ain_light = None
    ain_aux = None
    buzzer = None
    fan = None
    lamps = None
    servo = None
    switches = None
    temperature = None
    web_service = None

    def __init__(self):

        self._pi = pigpio.pi()             # exit script if no connection
        if not self._pi.connected:
            print("ERROR: unable to connect to pigpio")
            exit()
        self._read_config()
        self._make_components()

    def _read_config(self):
        """Load configuration file from user iot_gh directory.
        """
        try:
            config = configparser.ConfigParser()
            config.read(["iot_gh_system.conf", os.path.expanduser("~/iot_gh/iot_gh_system.conf")],encoding="UTF8")
            self.version = config["IOT_GREENHOUSE"]["VERSION"]
            self._url = config["IOT_GREENHOUSE"]["URL"]
            self._servo_ccw_limit = int(config["IOT_GREENHOUSE"]["SERVO_CCW_LIMIT"])
            self._servo_cw_limit = int(config["IOT_GREENHOUSE"]["SERVO_CW_LIMIT"])
        except :
            raise Exception("Unable to load IoT Greenhouse Systesm Configuration.")
       
    def _make_components(self):
        """Makes component services for IoT Greenhouse Service.
        """
        self.analog = GHAnalogService(self._pi)
        self.buzzer = GHBuzzer(self._pi, GHgpio.BUZZER)
        self.fan = GHFan(self._pi, GHgpio.FAN)
        self.lamps = GHLamps(self._pi, GHgpio.RED_LED, GHgpio.WHITE_LED, GHgpio.RED_LED, GHgpio.DUAL_LED)
        self.servo = GHServo(self._pi, GHgpio.SERVO_PWM, self._servo_cw_limit, self._servo_ccw_limit)
        self.switches = GHSwitches(self._pi, GHgpio.SWITCH_PB, GHgpio.SWITCH_TOGGLE)
        self.temperature = GHTemperature(self.analog.aux, self.analog.temp)
        self.web_service = GHWebService(self._url)    
        
    def make_greenhouse(self, name):
        """Factory class to build IoT Greenhouse data object.
        """
        gh = IoTGreenhouse()
        gh.name = name
        
        #read greenhouse config values
        config = configparser.ConfigParser()
        config.read(["iot_gh.conf", os.path.expanduser("~/iot_gh/iot_gh.conf")],encoding="UTF8")
        gh.house_id = config["IOT_GREENHOUSE"]["HOUSE_ID"]
        gh.row_id = config["IOT_GREENHOUSE"]["ROW_ID"]
        gh.group_id = config["IOT_GREENHOUSE"]["GROUP_ID"]
     
        self.update_state(gh)

        return gh
    
    def update_state(self, gh):
        """Updates IoTGreenhouse object by reading all house 
        states and refreshing gh object.
        """
        try:
    
            gh.led_red_state = self.lamps.red.get_state()
            gh.led_white_state = self.lamps.white.get_state()
            gh.led_dual_state =  self.lamps.dual.get_state()
            gh.switch_pb_state = self.switches.push_button.get_state()
            gh.switch_toggle_state = self.switches.toggle.get_state()
            gh.fan_state =  self.fan.get_state()
            gh.servo_position = self.servo.get_value()
            gh.buzzer_state = self.buzzer.get_state()
            gh.ain_pot_position = self.analog.pot.get_value()
            gh.ain_light_raw =  self.analog.light.get_value()
            gh.ain_aux_raw =  self.analog.aux.get_value()

            gh.temp_inside_C = self.temperature.inside_temp_C
            gh.temp_inside_F = self.temperature.inside_temp_F
            gh.temp_outside_C = self.temperature.outside_temp_C
            gh.temp_outside_F = self.temperature.outside_temp_F
            gh.temp_humidity = self.temperature.humidity
            gh.temp_reading_is_valid = self.temperature.reading_is_valid
            gh.temp_last_valid_reading = self.temperature.last_valid_read
            
            gh.valid_state = True
            gh.last_update = datetime.datetime.now()
        except Exception as e:
            gh.message = e.args[0]
            gh.valid_state = False
            gh.last_update = None

