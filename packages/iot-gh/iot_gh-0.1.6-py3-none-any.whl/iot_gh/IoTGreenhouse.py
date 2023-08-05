class IoTGreenhouse(object):
    """IoT Greenhouse data object"""
    #house IDs
    name = None
    house_id = None
    row_id = None
    group_id = None
    #house state
    valid_state = False
    last_update = None
    led_red_state = None
    led_white_state = None
    led_dual_state = None
    switch_pb_state = None
    switch_toggle_state = None
    fan_state = None
    servo_position = None
    buzzer_state = None
    ain_pot_position = None
    ain_light_raw = None
    ain_aux_raw = None
    temp_inside_C = 0
    temp_inside_F = 0
    temp_outside_C = 0
    temp_outside_F = 0
    temp_humidity =0
    temp_reading_is_valid = False
    temp_last_valid_reading = 0

    message = ""

    def __init__(self): 
        #use factory methond in IoTGreenhouse Service
        pass

    
