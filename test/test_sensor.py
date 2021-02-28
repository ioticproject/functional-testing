import pytest
import requests
from http import HTTPStatus
import json

from utils import Utils, HTTPClient
from config import (
    payload_client_account,
    ADD_SENSORS_URL,
    GET_SENSORS_URL,
    GET_USER_SENSORS_URL,
    GET_DEVICE_SENSORS_URL,
    DELETE_SENSORS_URL
)


@pytest.fixture(autouse=True)
def run_before_tests():
    pass


def test_post_sensor():
    with open('test/helper_jsons/new_sensor.json') as json_file:
        payload_json = json.load(json_file)
        payload_json["id_user"] = HTTPClient.global_id
        payload_json["id_device"] = HTTPClient.global_device_id
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post(url=ADD_SENSORS_URL,
                                       payload=payload,
                                       headers=headers)

        assert "id" in ret.json().keys()
        HTTPClient.sensor_id = int(ret.json()["id"])

        assert True


def test_post_sensor_invalid_uid():
    with open('test/helper_jsons/new_sensor.json') as json_file:
        payload_json = json.load(json_file)
        payload_json["id_user"] = -1
        payload_json["id_device"] = HTTPClient.global_device_id
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post_bad_request(url=ADD_SENSORS_URL,
                                                   payload=payload,
                                                   headers=headers)

        assert "Invalid user id" in ret.text


def test_post_sensor_invalid_devid():
    with open('test/helper_jsons/new_sensor.json') as json_file:
        payload_json = json.load(json_file)
        payload_json["id_user"] = HTTPClient.global_id
        payload_json["id_device"] = -1
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post_bad_request(url=ADD_SENSORS_URL,
                                                   payload=payload,
                                                   headers=headers)

        assert "Invalid device id" in ret.text


def test_get_sensors():
    with open('test/helper_jsons/admin_credentials.json') as json_file:
        payload_json = json.load(json_file)
        payload = str(payload_json).replace("\'", "\"")
        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }

        ret = HTTPClient.template_post(url=GET_SENSORS_URL,
                                       payload=payload,
                                       headers=headers,
                                       need_access_token=True)
        assert isinstance(ret.json(), list)
        assert True


def test_get_user_sensors():
    url = GET_USER_SENSORS_URL.format(ID=HTTPClient.global_id)
    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    ret = HTTPClient.template_get(url=url,
                                  payload={},
                                  headers=headers,
                                  need_access_token=True)
    assert isinstance(ret.json(), list)
    assert True


def test_get_device_sensors():
    url = GET_DEVICE_SENSORS_URL.format(ID=HTTPClient.global_id)
    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    ret = HTTPClient.template_get(url=url,
                                  payload={},
                                  headers=headers,
                                  need_access_token=True)
    assert isinstance(ret.json(), list)
    assert True


def test_delete_sensor():
    url = DELETE_SENSORS_URL.format(ID=HTTPClient.sensor_id)

    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    response = requests.request("DELETE", url, headers=headers, data={})
    assert response.status_code == HTTPStatus.OK
