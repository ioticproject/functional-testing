from test.utils import Utils, HTTPClient
from config import payload_client_account, payload_admin_account, LOGGER
import os
import shutil
import requests
from http import HTTPStatus
import time
import random

from config import (
    ADD_USER_URL,
    USER_LOGIN_URL,
    DELETE_USER_URL,
    ADD_DEVICE_URL,
    ADD_SENSORS_URL,
    ADD_DATA_URL,
    LOGGER,
    GET_USER_DEVICES_URL
)


def add_objects_for_tests():
    random_str = Utils.get_random_string(16)
    new_user_payload = str({"username": "admin",
                            "password": "123321123"
                            }).replace("\'", "\"")
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST",
                                url=USER_LOGIN_URL,
                                headers=headers,
                                data=new_user_payload)
    if response.status_code != HTTPStatus.CREATED:
        exit("[ERROR] Could not login user for testing.")
    HTTPClient.test_username = response.json()["username"]
    HTTPClient.test_password = response.json()["password"]
    HTTPClient.test_id = response.json()["_id"]
    HTTPClient.test_access_token = "jwt " + response.json()["access_token"]

    new_device_payload = str({"name": "test_device",
                              "id_user": HTTPClient.test_id,
                              "description": "description"
                              }).replace("\'", "\"")
    headers["Authorization"] = HTTPClient.test_access_token
    response = requests.request("POST",
                                url=ADD_DEVICE_URL.format(USER_ID=HTTPClient.test_id),
                                headers=headers,
                                data=new_device_payload)
    if not 'The device name already exists for this user.' in response.text:
        HTTPClient.test_device_id = response.json()["_id"]
    else:
        headers["Authorization"] = HTTPClient.test_access_token
        response = requests.request("GET", GET_USER_DEVICES_URL.format(USER_ID=HTTPClient.test_id),
                                    headers=headers,
                                    data={})
        devices = response.json().get("devices")
        for device in devices:
            if device["name"] == "test_device":
                HTTPClient.test_device_id = device["_id"]

    new_sensor_payload = str({"type": "test_sensor",
                              "measure_unit": "Celssius",
                              "id_user": HTTPClient.test_id,
                              "id_device": HTTPClient.test_device_id
                              }).replace("\'", "\"")
    headers["Authorization"] = HTTPClient.test_access_token
    response = requests.request("POST",
                                url=ADD_SENSORS_URL.format(USER_ID=HTTPClient.test_id,
                                                           DEVICE_ID=HTTPClient.test_device_id),
                                headers=headers,
                                data=new_sensor_payload)
    HTTPClient.test_sensor_id = response.json()["_id"]

if __name__ == '__main__':
    add_objects_for_tests()

    TIMEOUT = 2000
    url = ADD_DATA_URL.format(USER_ID=HTTPClient.test_id,
                              DEVICE_ID=HTTPClient.test_device_id,
                              SENSOR_ID=HTTPClient.test_sensor_id)
    headers = {"Authorization": HTTPClient.test_access_token,
               'Content-Type': 'application/json'}

    while TIMEOUT > 0:
        new_data_payload = str({"value": random.randint(1,1000)}).replace("\'", "\"")
        response = requests.request("POST",
                                    url=url,
                                    headers=headers,
                                    data=new_data_payload)
        print("Added new data for sensor " + str(HTTPClient.test_sensor_id))
        time.sleep(60)
        TIMEOUT -= 1
