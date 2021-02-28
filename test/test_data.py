import pytest
import requests
from http import HTTPStatus
import json

from utils import Utils, HTTPClient
from config import (
    payload_client_account,
    ADD_DATA_URL,
    GET_DATA_URL,
    GET_SENSOR_DATA_URL,
    GET_FILTERED_SENSOR_DATA_URL,
    DELETE_DATA_URL
)


@pytest.fixture(autouse=True)
def run_before_tests():
    pass


def test_post_data():
    with open('test/helper_jsons/new_data.json') as json_file:
        payload_json = json.load(json_file)
        payload_json["id_sensor"] = HTTPClient.global_sensor_id
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post(url=ADD_DATA_URL,
                                       payload=payload,
                                       headers=headers)

        assert "id" in ret.json().keys()
        HTTPClient.data_id = int(ret.json()["id"])

        assert True


def test_post_data_invalid_sensid():
    with open('test/helper_jsons/new_sensor.json') as json_file:
        payload_json = json.load(json_file)
        payload_json["id_sensor"] = -1
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post_bad_request(url=ADD_DATA_URL,
                                                   payload=payload,
                                                   headers=headers)

        assert "Invalid sensor id" in ret.text



def test_get_data():
    with open('test/helper_jsons/admin_credentials.json') as json_file:
        payload_json = json.load(json_file)
        payload = str(payload_json).replace("\'", "\"")
        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }

        ret = HTTPClient.template_post(url=GET_DATA_URL,
                                       payload=payload,
                                       headers=headers,
                                       need_access_token=True)
        assert isinstance(ret.json(), list)
        assert True


def test_get_sensor_data():
    url = GET_SENSOR_DATA_URL.format(ID=HTTPClient.global_sensor_id)
    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    ret = HTTPClient.template_get(url=url,
                                  payload={},
                                  headers=headers,
                                  need_access_token=True)
    assert isinstance(ret.json(), list)
    assert True


def test_get_filtered_sensor_data():
    url = GET_FILTERED_SENSOR_DATA_URL.format(ID=HTTPClient.global_id) + "?max_value=1500&min_value=700&from=2000-11-11"
    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    ret = HTTPClient.template_get(url=url,
                                  payload={},
                                  headers=headers,
                                  need_access_token=True)
    assert isinstance(ret.json(), list)
    print("_______________________________________________________________________")
    print(ret.text)

    url = GET_FILTERED_SENSOR_DATA_URL.format(ID=HTTPClient.global_id) + "?min_value=10&from=2000-11-11"
    headers = {
        'Authorization': HTTPClient.global_access_token
    }
    ret = HTTPClient.template_get(url=url,
                                  payload={},
                                  headers=headers,
                                  need_access_token=True)
    assert isinstance(ret.json(), list)
    print("_______________________________________________________________________")
    print(ret.text)

    assert True


def test_delete_data():
    url = DELETE_DATA_URL.format(ID=HTTPClient.data_id)

    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    response = requests.request("DELETE", url, headers=headers, data={})
    assert response.status_code == HTTPStatus.OK
