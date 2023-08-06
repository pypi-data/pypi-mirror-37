import spidev
import time
import os

class GHAnalogService(object):
    """Analog Service class for IoT Greenhouse

    Provides collection of 8 A/D inputs based on channel 
    definitions below
    """
    # Define sensor channels
    POT_CHANNEL  = 0
    LIGHT_CHANNEL  = 1
    TEMP_CHANNEL = 2
    AUX_CHANNEL = 3
    AD_IN_4_CHANNEL = 4
    AD_IN_5_CHANNEL = 5
    AD_IN_6_CHANNEL = 6
    AD_IN_7_CHANNEL = 7

    pot = None
    light = None
    temp = None
    aux = None
    ad_in_4 = None
    ad_in_5 = None
    ad_in_6 = None
    ad_in_7 = None

    _spi = None
    _pi = None  #currently not used

    def __init__(self, pi):
        """Constructor for class GHAnalogService
        
        :returns: AnalogService object
        """
        self._pi = pi
        # Open SPI bus
        self._spi = spidev.SpiDev()
        self._spi.open(0,0)
        self._spi.max_speed_hz=1000000
        
        self.pot = GHAnalogChannel(self._spi, self.POT_CHANNEL)
        self.light = GHAnalogChannel(self._spi, self.LIGHT_CHANNEL)
        self.temp = GHAnalogChannel(self._spi, self.TEMP_CHANNEL)
        self.aux = GHAnalogChannel(self._spi, self.AUX_CHANNEL)
        self.ad_in_4 = GHAnalogChannel(self._spi, self.AD_IN_4_CHANNEL)
        self.ad_in_5 = GHAnalogChannel(self._spi, self.AD_IN_5_CHANNEL)
        self.ad_in_6 = GHAnalogChannel(self._spi, self.AD_IN_6_CHANNEL)
        self.ad_in_7 = GHAnalogChannel(self._spi, self.AD_IN_7_CHANNEL)
 
 
class GHAnalogChannel(object):
    """Analog Channel class. Provides get functions to 
    read both raw digital and voltage values.
    """
    _spi = None
    _channel = None

    def __init__(self, spi, channel):
        self._spi = spi  
        self._channel = channel
        
    def get_value(self):
        adc = self._spi.xfer2([1,(8+self._channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

    # rounded to specified number of decimal places.
    def get_voltage(self, places):
        data = get_value()   
        volts = (data * 3.3) / float(1023)
        volts = round(volts, places)
        return volts

