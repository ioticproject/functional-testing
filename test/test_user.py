import pytest
import requests
from http import HTTPStatus
import json

from utils import Utils, HTTPClient
from config import (
    payload_client_account,
    HEALTH_URL,
    ADD_USER_URL,
    USER_LOGIN_URL,
    GET_USERS_URL,
    DELETE_USER_URL,
    UPDATE_USER_URL
)


@pytest.fixture(autouse=True)
def run_before_tests():
    pass


def test_health():
    payload = {}
    headers = {}

    response = requests.request("GET", HEALTH_URL, headers=headers, data=payload)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Healthy"


def test_post_user_invalid_passwd_format():
    with open('test/helper_jsons/new_user_credentials.json') as json_file:
        payload_json = json.load(json_file)
        payload_json["password"] = "1234"
        payload = str(payload_json).replace("\'", "\"")
        headers = {
            'Content-Type': 'application/json'
        }

        ret = HTTPClient.template_post_bad_request(url=ADD_USER_URL,
                                                   payload=payload,
                                                   headers=headers)
        assert "The password format is invalid." in ret.text


def test_post_user():
    with open('test/helper_jsons/new_user_credentials.json') as json_file:
        payload_json = json.load(json_file)
        payload = str(payload_json).replace("\'", "\"")
        headers = {
            'Content-Type': 'application/json'
        }

        ret = HTTPClient.template_post(url=ADD_USER_URL,
                                       payload=payload,
                                       headers=headers)
        HTTPClient.username = ret.json()["username"]
        HTTPClient.password = ret.json()["password"]
        HTTPClient.id = ret.json()["id"]

        assert True


def test_post_user_exists():
    with open('test/helper_jsons/new_user_credentials.json') as json_file:
        payload_json = json.load(json_file)
        payload = str(payload_json).replace("\'", "\"")
        headers = {
            'Content-Type': 'application/json'
        }

        ret = HTTPClient.template_post_bad_request(url=ADD_USER_URL,
                                                   payload=payload,
                                                   headers=headers)

        assert "The username already exists" in ret.text


def test_post_email_exists():
    with open('test/helper_jsons/new_user_credentials.json') as json_file:
        payload_json = json.load(json_file)
        payload_json["username"] = payload_json["username"] + "_new"

        payload = str(payload_json).replace("\'", "\"")

        headers = {
            'Content-Type': 'application/json'
        }

        ret = HTTPClient.template_post_bad_request(url=ADD_USER_URL,
                                                   payload=payload,
                                                   headers=headers)

        assert "The email was already associated with another account" in ret.text


def test_login():
    payload_json = {
        "username": HTTPClient.username,
        "password": HTTPClient.password
    }
    payload = str(payload_json).replace("\'", "\"")
    headers = {
        'Content-Type': 'application/json'
    }

    ret = HTTPClient.template_post(url=USER_LOGIN_URL,
                                   payload=payload,
                                   headers=headers)
 
    HTTPClient.access_token = "jwt " + ret.json()["access_token"]

    assert True


def test_get_users():
    with open('test/helper_jsons/admin_credentials.json') as json_file:
        payload_json = json.load(json_file)
        payload = str(payload_json).replace("\'", "\"")
        headers = {
            'Content-Type': 'application/json',
            'Authorization': HTTPClient.access_token
        }

        ret = HTTPClient.template_post(url=GET_USERS_URL,
                                       payload=payload,
                                       headers=headers,
                                       need_access_token=True)
        assert isinstance(ret.json(), list)
        assert True


def test_put_user():
    url = UPDATE_USER_URL.format(ID=HTTPClient.id)

    payload = "{\"password\": \"test_new_password!1234\"}"
    headers = {
        'Authorization': HTTPClient.access_token,
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    assert response.status_code == HTTPStatus.OK

    # Check if after the old password was changed, the user can login
    # with the new one
    payload_json = {
        "username": HTTPClient.username,
        "password": "test_new_password!1234"
    }
    payload = str(payload_json).replace("\'", "\"")
    headers = {
        'Content-Type': 'application/json'
    }

    HTTPClient.template_post(url=USER_LOGIN_URL,
                             payload=payload,
                             headers=headers)


def test_delete_user():
    url = DELETE_USER_URL.format(ID=HTTPClient.id)

    headers = {
        'Authorization': HTTPClient.access_token
    }

    response = requests.request("DELETE", url, headers=headers, data={})
    assert response.status_code == HTTPStatus.OK
