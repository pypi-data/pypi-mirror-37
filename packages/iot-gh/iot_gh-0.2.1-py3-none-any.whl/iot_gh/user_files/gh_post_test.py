from iot_gh.IoTGreenhouse import IoTGreenhouse
from iot_gh.IoTGreenhouseService import IoTGreenhouseService


ghs = None      #iot_greenhouse_service
gh = None       #iot_greenhouse data object

def test_post():
    global ghs
    
    print("*** GH testing ***")   
    ghs = IoTGreenhouseService()
    gh = ghs.make_greenhouse("test")
    gh.message = "test post"

    print("status code = %i" % gh.post_data.statuscode)
    print("GH post test completed.")   

if __name__ == "__main__":
    test_post()



