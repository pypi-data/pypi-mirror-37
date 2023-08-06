from time import time
import requests
import json

class GHPostData():
    """Data object for post response
    """
    statuscode = 0
    last_update = None
    exception = None

class GHWebService(object):
    """ Web connector for Flow service. Post data using json package.
    """
    url = None

    def __init__(self, url):
        self.url = url
        
    def post_greenhouse(self, greenhouse):

        if greenhouse.post_data == None or time() > greenhouse.post_data.last_update + 20:
            payload = self._make_payload(greenhouse)
            self._post_data(payload)
        
    def _make_payload(self, greenhouse):
        
        payload = json.dumps(greenhouse.__dict__)
        #payload = {
        #    "house_ID": greenhouse.settings.house_ID,
        #    "row_id": greenhouse.settings.row_id,
        #    "group_ID": greenhouse.settings.group_ID,
        #    "version":  greenhouse.settings.version,
        #    "name": greenhouse.name,
        #    "led_red_state": greenhouse.led_red_state,
        #    "led_white_state": greenhouse.led_white_state,
        #    "led_dual_state":  greenhouse.led_dual_state,
        #    "switch_pb_state":  greenhouse.switch_pb_state,
        #    "switch_toggle_state": greenhouse.switch_toggle_state,
        #    "fan_state": greenhouse.fan_state,
        #    "servo_position":  greenhouse.servo_position,
        #    "buzzer_state": greenhouse.buzzer_state,
        #    "ain_pot_position": greenhouse.ain_pot_position,
        #    "ain_light_raw":  greenhouse.ain_light_raw,
        #    "ain_aux_raw": greenhouse.ain_aux_raw,

        #    "temp_inside_C":  greenhouse.temp_inside_C,
        #    "temp_inside_F": greenhouse.temp_inside_F,
        #    "temp_outside_C":  greenhouse.temp_outside_C,
        #    "temp_outside_F": greenhouse.temp_outside_F,
        #    #"temp_humidity": greenhouse.temp_humidity,
        #    #"temp_reading_is_valid":  greenhouse.temp_reading_is_valid,
        #    #"temp_last_valid_reading":  greenhouse.temp_last_valid_reading,
            
        #    "valid_state": greenhouse.valid_state,
        #    "last_update": greenhouse.last_update
        #    }

        return payload
            
    def _post_data(self, payload):       
        try:
            headers = {'content-type': 'application/json'}
            r = requests.post(self.url, json=payload, headers=headers)
            _gh.post_data.statuscode = r.status_code
            _gh.post_data.last_update = time.time()
            
        except Exception as ex:
            print("Error: Unable to post data to service. Check for valid Wi-Fi connection.")
            _gh.post_data.exception = ex 
        else:
            pass


def test_post():
    from iot_gh.IoTGreenhouseService import IoTGreenhouseService
    
    ghs = IoTGreenhouseService()
    gh = ghs.make_greenhouse("test")
    ws = GHWebService(ghs._url)
    
    ws.post_greenhouse(gh)
    print(gh.post_data.statuscode)
    print(gh.post_data.last_update)
    print(gh.post_data.exception)
    
if __name__ == "__main__":
    test_post()