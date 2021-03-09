import pytest
import requests
from http import HTTPStatus
import json

from utils import HTTPClient, Utils
from config import (
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
        url = ADD_DATA_URL.format(USER_ID=HTTPClient.global_id,
                                  DEVICE_ID=HTTPClient.global_device_id,
                                  SENSOR_ID=HTTPClient.global_sensor_id)

        payload_json = json.load(json_file)
        payload_json["id_sensor"] = HTTPClient.global_sensor_id
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post(url=url,
                                       payload=payload,
                                       headers=headers)

        assert "_id" in ret.json().keys()
        HTTPClient.data_id = ret.json()["_id"]

        assert True


def test_post_data_inconsistent_sensor_id():
    with open('test/helper_jsons/new_data.json') as json_file:
        url = ADD_DATA_URL.format(USER_ID=HTTPClient.global_id,
                                  DEVICE_ID=HTTPClient.global_device_id,
                                  SENSOR_ID=HTTPClient.global_sensor_id)

        payload_json = json.load(json_file)
        payload_json["id_sensor"] = "INVALID"
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = HTTPClient.template_post_bad_request(url=url,
                                                   payload=payload,
                                                   headers=headers)

        assert "The sensor id from the url does not correspond with the one from the payload." in ret.text


def test_post_sensor_inexistent_sensor_id():
    with open('test/helper_jsons/new_sensor.json') as json_file:
        url = ADD_DATA_URL.format(USER_ID=HTTPClient.global_id,
                                  DEVICE_ID=HTTPClient.global_device_id,
                                  SENSOR_ID="INVALID")

        payload_json = json.load(json_file)
        payload_json["id_user"] = HTTPClient.global_id
        payload_json["id_device"] = HTTPClient.global_device_id
        payload_json["id_sensor"] = "INVALID"
        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.global_access_token
        }
        ret = requests.request("POST",
                               url=url,
                               headers=headers,
                               data=payload)

        assert ret.status_code == HTTPStatus.NOT_FOUND
        assert "The sensor id does not exist." in ret.text


def test_get_data():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': HTTPClient.admin_access_token
    }

    ret = HTTPClient.template_get(url=GET_DATA_URL,
                                  payload={},
                                  headers=headers,
                                  need_access_token=True)
    assert 'data' in ret.json().keys()
    assert isinstance(ret.json().get('data'), list)


def test_get_sensor_data():
    url = GET_SENSOR_DATA_URL.format(USER_ID=HTTPClient.global_id,
                                     DEVICE_ID=HTTPClient.global_device_id,
                                     SENSOR_ID=HTTPClient.global_sensor_id)
    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    ret = HTTPClient.template_get(url=url,
                                  payload={},
                                  headers=headers,
                                  need_access_token=True)
    assert 'data' in ret.json().keys()
    assert isinstance(ret.json().get('data'), list)


def test_get_filtered_sensor_data():
    query_str1 = "?max_value=1500&min_value=700&from=2000-11-11"
    query_str2 = "?from=2000-11-11"
    url = GET_FILTERED_SENSOR_DATA_URL.format(USER_ID=HTTPClient.global_id,
                                              DEVICE_ID=HTTPClient.global_device_id,
                                              SENSOR_ID=HTTPClient.global_sensor_id)
    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    ret = HTTPClient.template_get(url=url + query_str1,
                                  payload={},
                                  headers=headers,
                                  need_access_token=True)
    assert 'data' in ret.json().keys()
    assert isinstance(ret.json().get('data'), list)

    # ret = HTTPClient.template_get(url=url + query_str2,
    #                               payload={},
    #                               headers=headers,
    #                               need_access_token=True)
    # assert isinstance(ret.json(), list)


def test_delete_data_unauthorized():
    url = DELETE_DATA_URL.format(USER_ID=HTTPClient.global_id,
                                 DEVICE_ID=HTTPClient.global_device_id,
                                 SENSOR_ID=HTTPClient.global_sensor_id,
                                 ID=HTTPClient.data_id)

    headers = {
        'Authorization': Utils.get_random_token()
    }

    assert requests.request("DELETE",
                            url,
                            headers=headers,
                            data={}).status_code == HTTPStatus.UNAUTHORIZED


def test_delete_data():
    url = DELETE_DATA_URL.format(USER_ID=HTTPClient.global_id,
                                 DEVICE_ID=HTTPClient.global_device_id,
                                 SENSOR_ID=HTTPClient.global_sensor_id,
                                 ID=HTTPClient.data_id)

    headers = {
        'Authorization': HTTPClient.global_access_token
    }

    response = requests.request("DELETE",
                                url=url,
                                headers=headers,
                                data={})
    assert response.status_code == HTTPStatus.OK
