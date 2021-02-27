from utils import generate_access_token
from utils import SharedValues
import sys
from config import payload_client_account, payload_admin_account
import os
import glob
from utils import get_random_string

# RUN BEFORE ALL TESTS
def pytest_sessionstart(session):
    generate_access_token()
    if SharedValues.access_token is None:
        sys.exit("[ERROR] Could not fetch the access token.")
        
    with open("test/helper_jsons/admin_credentials.json", 'w') as f:
        f.write(payload_admin_account)
    
    with open("test/helper_jsons/user_credentials.json", 'w') as f:
        f.write(payload_client_account)
    
    with open("test/helper_jsons/new_user_credentials.json", 'w') as f:
        random_str = "TEST" + get_random_string(8)
        new_user_payload = str({ "username": random_str,
                    "password": "!!" + random_str,
                    "email": random_str + "@outlook.com"
                }).replace("\'", "\"")
        f.write(new_user_payload)
    
    with open("test/helper_jsons/new_device.json", 'w') as f:
        random_str = "TEST" + get_random_string(8)
        new_user_payload = str({ "name": random_str,
                                "id_user": 2,
                                "description": random_str}
                               ).replace("\'", "\"")
        f.write(new_user_payload)
    
    with open("test/helper_jsons/new_sensor.json", 'w') as f:
        random_str = "TEST" + get_random_string(8)
        new_user_payload = str({"type": "temperature",
                                "measuremUnit": "celssius",
                                "id_user": 4,
                                "id_device": 4}).replace("\'", "\"")
        f.write(new_user_payload)
    
    with open("test/helper_jsons/new_data.json", 'w') as f:
        new_user_payload = str({ "id_sensor": 2,
                                "value": 2000}
                               ).replace("\'", "\"")
        f.write(new_user_payload)
    

def pytest_sessionfinish(session):
    files = glob.glob("test/helper_jsons", recursive=True)

    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))