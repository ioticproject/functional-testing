import pytest
import requests
from http import HTTPStatus
import json

from utils import Utils, HTTPClient
from config import (
    payload_client_account,
    ADD_DEVICE_URL,
    GET_DEVICES_URL,
    GET_DEVICE_URL,
    GET_USER_DEVICES_URL,
    DELETE_DEVICE_URL,
    LOGGER
)


@pytest.fixture(autouse=True)
def run_before_tests():
    pass


def test_post_device():
    with open('test/helper_jsons/new_device.json') as json_file:
        url = ADD_DEVICE_URL.format(USER_ID=HTTPClient.global_id)

        payload_json = json.load(json_file)
        payload_json["id_user"] = HTTPClient.global_id
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }

        ret = HTTPClient.template_post(url=url,
                                       payload=payload,
                                       headers=headers)

        assert "id" in ret.json().keys()
        HTTPClient.device_id = ret.json()["id"]


def test_post_device_exists():
    with open('test/helper_jsons/new_device.json') as json_file:
        url = ADD_DEVICE_URL.format(USER_ID=HTTPClient.global_id)

        payload_json = json.load(json_file)
        payload_json["id_user"] = HTTPClient.global_id
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post_bad_request(url=url,
                                                   payload=payload,
                                                   headers=headers)

        assert "The device name already exists for this user" in ret.text


def test_post_device_inexistent_user_id():
    with open('test/helper_jsons/new_device.json') as json_file:
        url = ADD_DEVICE_URL.format(USER_ID="------------")

        payload_json = json.load(json_file)
        payload_json["id_user"] = "------------"
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = requests.request("POST", url, headers=headers, data=payload)
        assert ret.status_code == HTTPStatus.UNAUTHORIZED
        assert "The authorization token does not belong to you." in ret.json().get("error")


def test_post_device_inconsistent_user_id():
    with open('test/helper_jsons/new_device.json') as json_file:
        url = ADD_DEVICE_URL.format(USER_ID=HTTPClient.global_id)

        payload_json = json.load(json_file)
        payload_json["id_user"] = -1
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post_bad_request(url=url,
                                                   payload=payload,
                                                   headers=headers)

        assert "The user id from the url does not correspond with the one from the payload." in ret.text


def test_get_devices():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': HTTPClient.admin_access_token
    }

    ret = HTTPClient.template_get(url=GET_DEVICES_URL,
                                    payload={},
                                    headers=headers,
                                    need_access_token=True)
    assert isinstance(ret.json(), list)


def test_get_device():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': HTTPClient.global_access_token
    }

    url = GET_DEVICE_URL.format(USER_ID=HTTPClient.global_id, ID=HTTPClient.device_id)
    ret = HTTPClient.template_get(url=url,
                                  payload={},
                                  headers=headers,
                                  need_access_token=True)

    assert {"description", "id_user", "id", "name"}.issubset(ret.json().keys())


def test_get_user_devices():
    url = GET_USER_DEVICES_URL.format(USER_ID=HTTPClient.global_id)
    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    ret = HTTPClient.template_get(url=url,
                                  payload={},
                                  headers=headers,
                                  need_access_token=True)
    assert isinstance(ret.json(), list)


def test_delete_device():
    url = DELETE_DEVICE_URL.format(USER_ID=HTTPClient.global_id,
                                   ID=HTTPClient.device_id)

    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    response = requests.request("DELETE",
                                url=url,
                                headers=headers,
                                data={})
    assert response.status_code == HTTPStatus.OK
