from utils import Utils, HTTPClient
from config import payload_client_account, payload_admin_account, LOGGER
import os
import shutil
import requests
from http import HTTPStatus

from config import (
    ADD_USER_URL,
    DELETE_USER_URL,
    ADD_DEVICE_URL,
    ADD_SENSORS_URL
)


def add_objects_for_tests():
    # Add global user for the device and sensor tests
    random_str = Utils.get_random_string(16)
    new_user_payload = str({"username": "TEST-" + random_str,
                            "password": "!!" + random_str,
                            "email": random_str + "@test.com"
                            }).replace("\'", "\"")
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST",
                                url=ADD_USER_URL,
                                headers=headers,
                                data=new_user_payload)
    if response.status_code != HTTPStatus.CREATED:
        exit("[ERROR] Could not add user for testing.")
    HTTPClient.global_username = response.json()["username"]
    HTTPClient.global_password = response.json()["password"]
    HTTPClient.global_id = response.json()["_id"]
    LOGGER.info("Added user for testing.")

    # Generate access token
    HTTPClient.generate_access_token(username=HTTPClient.global_username,
                                     password=HTTPClient.global_password)

    # Add global device for the data and sensors tests
    new_device_payload = str({"name": "TEST-" + random_str,
                              "id_user": HTTPClient.global_id,
                              "description": random_str
                              }).replace("\'", "\"")
    headers["Authorization"] = HTTPClient.global_access_token
    response = requests.request("POST",
                                url=ADD_DEVICE_URL.format(USER_ID=HTTPClient.global_id),
                                headers=headers,
                                data=new_device_payload)
    if response.status_code != HTTPStatus.CREATED:
        exit("[ERROR] Could not add device for testing." + response.text)
    HTTPClient.global_device_id = response.json()["_id"]
    LOGGER.info("Added device for testing.")

    # Add global sensor for the data tests
    new_sensor_payload = str({"type": "TEST-" + random_str,
                              "measure_unit": "Celssius",
                              "id_user": HTTPClient.global_id,
                              "id_device": HTTPClient.global_device_id
                              }).replace("\'", "\"")
    headers["Authorization"] = HTTPClient.global_access_token
    response = requests.request("POST",
                                url=ADD_SENSORS_URL.format(USER_ID=HTTPClient.global_id,
                                                           DEVICE_ID=HTTPClient.global_device_id),
                                headers=headers,
                                data=new_sensor_payload)
    if response.status_code != HTTPStatus.CREATED:
        exit("[ERROR] Could not add sensor for testing. " + response.text)
    HTTPClient.global_sensor_id = response.json()["_id"]
    LOGGER.info("Added sensor for testing.")


def generate_payload_files():
    with open("test/helper_jsons/admin_credentials.json", 'w') as f:
        f.write(payload_admin_account)

    with open("test/helper_jsons/user_credentials.json", 'w') as f:
        f.write(payload_client_account)

    with open("test/helper_jsons/new_user_credentials.json", 'w') as f:
        random_str = Utils.get_random_string(16)
        new_user_payload = str({ "username": "TEST-" + random_str,
                    "password": "!!" + random_str,
                    "email": random_str + "@test.com"
                }).replace("\'", "\"")
        f.write(new_user_payload)

    with open("test/helper_jsons/new_device.json", 'w') as f:
        random_str = "TEST-" + Utils.get_random_string(16)
        new_user_payload = str({ "name": random_str,
                                "id_user": 2,
                                "description": random_str}
                               ).replace("\'", "\"")
        f.write(new_user_payload)

    with open("test/helper_jsons/new_sensor.json", 'w') as f:
        random_str = "TEST-" + Utils.get_random_string(16)
        new_user_payload = str({"type": "temperature",
                                "measure_unit": "celssius",
                                "id_user": 4,
                                "id_device": 4}).replace("\'", "\"")
        f.write(new_user_payload)

    with open("test/helper_jsons/new_data.json", 'w') as f:
        new_user_payload = str({"id_sensor": 2,
                                "value": 2000}
                               ).replace("\'", "\"")
        f.write(new_user_payload)


def remove_dir_content(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# RUN BEFORE ALL TESTS
def pytest_sessionstart(session):
    generate_payload_files()
    add_objects_for_tests()


def pytest_sessionfinish(session):
    remove_dir_content("test/helper_jsons")

    headers = {
        'Authorization': HTTPClient.global_access_token
    }
    response = requests.request("DELETE",
                                url=DELETE_USER_URL.format(ID=HTTPClient.global_id),
                                headers=headers,
                                data={})
    if response.status_code != HTTPStatus.OK:
        exit("[Error] Could not delete the test user. The database may be polluted" + response.text)