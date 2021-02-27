import pytest
import requests
from http import HTTPStatus
import json

import sys

from utils import Utils, HTTPClient
from config import (
    payload_client_account,
    HEALTH_URL,
    ADD_USER_URL,
    USER_LOGIN_URL,
    GET_USERS_URL,
    ADD_USER_URL,
    DELETE_USER_URL,
    UPDATE_USER_URL
)


@pytest.fixture(autouse=True)
def run_before_tests():
    pass


def test_health():
    payload={}
    headers = {}

    response = requests.request("GET", HEALTH_URL, headers=headers, data=payload)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Healthy"


def test_post_user():
    with open('test/helper_jsons/user_credentials.json') as json_file:
        payload_json = json.load(json_file)
        payload_json['username'] = "TEST_" + Utils.generate_random_string(24)
        payload_json['username'] = "TEST_" + payload_json['username'] + "@test.com"

        payload = str(payload_json)
        headers = {
        'Content-Type': 'application/json'
        }

        HTTPClient.template_post(url=ADD_USER_URL,
                                payload=payload,
                                headers=headers)
        assert True


# def test_login():
#     json_path = str('test/helper_jsons/user_credentials.json')
#     HTTPClient.template_get(url=USER_LOGIN_URL,
#                             payload = 'user_login',
#                   json_path=json_path)
    

#     assert True


# def test_get_users():
#     json_path = str('test/helper_jsons/admin_credentials.json')
#     template_post(GET_USERS_URL,
#                   'get_users',
#                   json_path=json_path)

#     assert True


# def test_add_user():
#     json_path = str('test/helper_jsons/new_user_credentials.json')
#     template_post(ADD_USER_URL,
#                   'add_user',
#                   json_path=json_path)

#     assert True
