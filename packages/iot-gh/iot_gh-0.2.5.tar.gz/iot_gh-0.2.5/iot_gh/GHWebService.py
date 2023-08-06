from time import time
import requests
import json
import ast
 
class GHPostData():
    """Data object for post response
    """
    status_code = 0
    last_update = None
    exception = None

class GHWebService(object):
    """ Web connector for Flow service. Post data using json package.
    """
    url = None

    def __init__(self, url):
        self.url = url
        
    def post_greenhouse(self, greenhouse):
        #throttle post to every 30 sec
        if greenhouse.post_data == None or time() > greenhouse.post_data.last_update + 30:
            p_data = self._post(greenhouse)
            greenhouse.post_data = p_data

               
    def _post(self, gh, verbose=False):
        '''HTTP request post of json dump

        json package formated for Flow service
        '''
        post_data = GHPostData()
        try:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            if verbose:
                payload = json.dumps(gh.__dict__)
            else:
                payload = {"house_id": gh.house_id, 
                          "group_id": gh.group_id, 
                          "house_number": gh.house_number,
                          "name": gh.name,
                          "temp_inside_F": gh.temp_inside_F,
                          "temp_outside_F": gh.temp_outside_F,
                          "servo_status": gh.servo_status,
                          "fan_status": gh.fan_status,
                          "heater_status": gh.led_white_status,  #white led simulates heater

                          "message": gh.message}

            json_payload = ast.literal_eval(payload)
            r = requests.post(self.url, json=json_payload , headers=headers)
            post_data.status_code = r.status_code
            post_data.last_update = time()
            
        except Exception as ex:
            print("Error: Unable to post data to service. Check for valid Wi-Fi connection. %s" % ex.args[0])
            post_data.exception = ex 
        
        finally:
            return post_data


def test_post():
    from iot_gh.IoTGreenhouseService import IoTGreenhouseService

    ghs = IoTGreenhouseService()
    gh = ghs.make_greenhouse("test")
    ws = GHWebService(ghs._url)
    ws.post_greenhouse(gh)
    print(gh.post_data.status_code)
    print(gh.post_data.last_update)
    print(gh.post_data.exception)
    
if __name__ == "__main__":
    test_post()