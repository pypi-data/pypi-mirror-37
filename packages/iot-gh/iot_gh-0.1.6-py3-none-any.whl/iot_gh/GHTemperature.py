import threading
from time import sleep
#from GH.dht11 import DHT11 #Current config is using two analog sensors

class GHTemperature(object):
    """This class GHFan provides a services to read IoT Greenhouse temperature.
    """
    
    _analogTempSensor_in = None
    _analogTempSensor_out = None

    def __init__(self, analog_temp_channel_in, analog_temp_channel_out):
        """Constructor for class GHTemperature service
        
        Wrapper class for analog temperature channels
        :param analog_temp_channel_in: reference to inside temperature analog channel
        :param analog_temp_channel_out: reference to outside temperature analog channel
        :returns: GHTemperature object
        """
        self._analogTempSensor_in = analog_temp_channel_in
        self._analogTempSensor_out = analog_temp_channel_out
        

    def convert_C_to_F(self, temp_C):
        return temp_C * 9/5 +32

    def convert_F_to_C(self, temp_F):
        return (temp_F - 32) * 5/9

    # Function to calculate temperature from
    # TMP36 data, rounded to specified
    # number of decimal places.
    def _convert_to_temp(self, data, places):
 
      # ADC Value
      # (approx)  Temp  Volts
      #    0      -50    0.00
      #   78      -25    0.25
      #  155        0    0.50
      #  233       25    0.75
      #  310       50    1.00
      #  465      100    1.50
      #  775      200    2.50
      # 1023      280    3.30
 
      temp = ((data * 330)/float(1023))-50
      temp = round(temp,places)
      return temp

    def get_inside_temp_C(self):
         analog_value = self._analogTempSensor_in.get_value()
         temp_value_C = self._convert_to_temp(analog_value, 1)
         return temp_value_C

    def get_inside_temp_F(self):
        temp_value_F = self.convert_C_to_F(self.get_inside_temp_C()) 
        return temp_value_F

    def get_outside_temp_C(self):
         analog_value = self._analogTempSensor_out.get_value()
         temp_value_C = self._convert_to_temp(analog_value, 1)
         return temp_value_C

    def get_outside_temp_F(self):
        temp_value_F = self.convert_C_to_F(self.get_outside_temp_C()) 
        return temp_value_F
