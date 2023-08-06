from iot_gh.IoTGreenhouse import IoTGreenhouse
from iot_gh.IoTGreenhouseService import IoTGreenhouseService

def test_post():
   
    print("*** GH testing ***")   
    ghs = IoTGreenhouseService()
    gh = ghs.greenhouse
    ghs.web_service.post_greenhouse()
    print(gh.post_data.status_code)
    print(gh.post_data.last_update)
    print(gh.post_data.exception)
    print("GH post test completed.")   

if __name__ == "__main__":
    test_post()



