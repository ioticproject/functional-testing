import pytest
import requests
from http import HTTPStatus
import json

from utils import Utils, HTTPClient
from config import (
    ADD_SENSORS_URL,
    GET_SENSORS_URL,
    GET_SENSOR_URL,
    GET_USER_SENSORS_URL,
    GET_DEVICE_SENSORS_URL,
    DELETE_SENSORS_URL
)


@pytest.fixture(autouse=True)
def run_before_tests():
    pass


def test_post_sensor():
    with open('test/helper_jsons/new_sensor.json') as json_file:
        url = ADD_SENSORS_URL.format(USER_ID=HTTPClient.global_id,
                                     DEVICE_ID=HTTPClient.global_device_id)

        payload_json = json.load(json_file)
        payload_json["id_user"] = HTTPClient.global_id
        payload_json["id_device"] = HTTPClient.global_device_id
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post(url=url,
                                       payload=payload,
                                       headers=headers)

        assert "_id" in ret.json().keys()
        HTTPClient.sensor_id = ret.json()["_id"]

        assert True


def test_post_sensor_invalid_user_id():
    with open('test/helper_jsons/new_sensor.json') as json_file:
        url = ADD_SENSORS_URL.format(USER_ID=HTTPClient.global_id,
                                     DEVICE_ID=HTTPClient.global_device_id)

        payload_json = json.load(json_file)
        payload_json["id_user"] = "INVALID"
        payload_json["id_device"] = HTTPClient.global_device_id
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post_bad_request(url=url,
                                                   payload=payload,
                                                   headers=headers)
        assert "The user id from the url does not correspond with the one from the payload." in ret.text


def test_post_sensor_inconsistent_device_id():
    with open('test/helper_jsons/new_sensor.json') as json_file:
        url = ADD_SENSORS_URL.format(USER_ID=HTTPClient.global_id,
                                     DEVICE_ID=HTTPClient.global_device_id)

        payload_json = json.load(json_file)
        payload_json["id_user"] = HTTPClient.global_id
        payload_json["id_device"] = "INVALID"
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post_bad_request(url=url,
                                                   payload=payload,
                                                   headers=headers)

        assert "The device id from the url does not correspond with the one from the payload." in ret.text


def test_post_sensor_inexistent_device_id():
    with open('test/helper_jsons/new_sensor.json') as json_file:
        url = ADD_SENSORS_URL.format(USER_ID=HTTPClient.global_id,
                                     DEVICE_ID="INVALID")

        payload_json = json.load(json_file)
        payload_json["id_user"] = HTTPClient.global_id
        payload_json["id_device"] = "INVALID"
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = requests.request("POST", url, headers=headers, data=payload)
        assert ret.status_code == HTTPStatus.NOT_FOUND
        assert "The device id does not exist for this user." in ret.text


def test_get_sensors():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': HTTPClient.admin_access_token
    }

    ret = HTTPClient.template_get(url=GET_SENSORS_URL,
                                  payload={},
                                  headers=headers,
                                  need_access_token=True)

    assert 'sensors' in ret.json().keys()
    assert isinstance(ret.json().get('sensors'), list)


def test_get_sensor():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': HTTPClient.global_access_token
    }

    url = GET_SENSOR_URL.format(USER_ID=HTTPClient.global_id,
                                DEVICE_ID=HTTPClient.global_device_id,
                                ID=HTTPClient.sensor_id)
    ret = HTTPClient.template_get(url=url,
                                  payload={},
                                  headers=headers,
                                  need_access_token=True)
    assert {"measure_unit", "type", "data", "id_user", "_id", "id_device"}.issubset(ret.json().keys())



def test_get_user_sensors():
    url = GET_USER_SENSORS_URL.format(USER_ID=HTTPClient.global_id,
                                      ID=HTTPClient.global_id)
    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    ret = HTTPClient.template_get(url=url,
                                  payload={},
                                  headers=headers,
                                  need_access_token=True)
    assert 'sensors' in ret.json().keys()
    assert isinstance(ret.json().get('sensors'), list)
    assert True


def test_get_device_sensors():
    url = GET_DEVICE_SENSORS_URL.format(USER_ID=HTTPClient.global_id,
                                        DEVICE_ID=HTTPClient.global_device_id)
    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    ret = HTTPClient.template_get(url=url,
                                  payload={},
                                  headers=headers,
                                  need_access_token=True)
    assert 'sensors' in ret.json().keys()
    assert isinstance(ret.json().get('sensors'), list)
    assert True


def test_delete_sensor_unauthorized():
    url = DELETE_SENSORS_URL.format(USER_ID=HTTPClient.global_id,
                                    DEVICE_ID=HTTPClient.global_device_id,
                                    ID=HTTPClient.sensor_id)

    headers = {
        'Authorization': Utils.get_random_token()
    }

    assert requests.request("DELETE",
                            url,
                            headers=headers,
                            data={}).status_code == HTTPStatus.UNAUTHORIZED


def test_delete_sensor():
    url = DELETE_SENSORS_URL.format(USER_ID=HTTPClient.global_id,
                                    DEVICE_ID=HTTPClient.global_device_id,
                                    ID=HTTPClient.sensor_id)

    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    response = requests.request("DELETE", url, headers=headers, data={})
    assert response.status_code == HTTPStatus.OK
