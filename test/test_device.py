import pytest
import requests
from http import HTTPStatus
import json

from utils import Utils, HTTPClient
from config import (
    payload_client_account,
    ADD_DEVICE_URL,
    GET_DEVICES_URL,
    GET_USER_DEVICES_URL,
    DELETE_DEVICE_URL, 
    LOGGER
)


@pytest.fixture(autouse=True)
def run_before_tests():
    pass


def test_post_device():
    with open('test/helper_jsons/new_device.json') as json_file:
        payload_json = json.load(json_file)
        payload_json["id_user"] = HTTPClient.global_id
        payload = str(payload_json).replace("\'", "\"")
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post(url=ADD_DEVICE_URL,
                                       payload=payload,
                                       headers=headers)

        assert "id" in ret.json().keys()
        HTTPClient.device_id = ret.json()["id"]

        assert True


def test_post_device_exists():
    with open('test/helper_jsons/new_device.json') as json_file:
        payload_json = json.load(json_file)
        payload_json["id_user"] = HTTPClient.global_id
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post_bad_request(url=ADD_DEVICE_URL,
                                                   payload=payload,
                                                   headers=headers)

        assert "The device name already exists for this user" in ret.text


def test_post_device_invalid_uid():
    with open('test/helper_jsons/new_device.json') as json_file:
        payload_json = json.load(json_file)
        payload_json["id_user"] = -1
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post_bad_request(url=ADD_DEVICE_URL,
                                                   payload=payload,
                                                   headers=headers)

        assert "Invalid user id" in ret.text


def test_get_devices():
    with open('test/helper_jsons/admin_credentials.json') as json_file:
        payload_json = json.load(json_file)
        payload = str(payload_json).replace("\'", "\"")
        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }

        ret = HTTPClient.template_post(url=GET_DEVICES_URL,
                                       payload=payload,
                                       headers=headers,
                                       need_access_token=True)
        assert isinstance(ret.json(), list)
        assert True


def test_get_user_devices():
    url = GET_USER_DEVICES_URL.format(ID=HTTPClient.global_id)
    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    ret = HTTPClient.template_get(url=url,
                                   payload={},
                                   headers=headers,
                                   need_access_token=True)
    assert isinstance(ret.json(), list)
    assert True


def test_delete_device():
    url = DELETE_DEVICE_URL.format(ID=HTTPClient.device_id)

    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    response = requests.request("DELETE", url, headers=headers, data={})
    assert response.status_code == HTTPStatus.OK
