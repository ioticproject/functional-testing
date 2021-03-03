import random
import string
import subprocess
from http import HTTPStatus

import requests
from config import (AUTH_URL, LOGGER, payload_admin_account)



class HTTPClient:
    access_token = None
    global_access_token = None

    def generate_access_token():
        url = AUTH_URL
        headers = {'Content-Type': 'application/json'}

        response = requests.request(
            method='POST',
            url=url,
            headers=headers,
            data=payload_admin_account
        )

        if response.status_code != HTTPStatus.OK:
            LOGGER.critical('POST status code = ' + str(response.status_code))
            return

        HTTPClient.global_access_token = "jwt " + response.json()['access_token']
        LOGGER.info('Got the intra access token: ' + HTTPClient.global_access_token)


    def template_get(url, headers, payload, need_access_token=False):
        response = requests.request("GET", url, headers=headers, data=payload)
        assert (
            response.status_code == HTTPStatus.OK
            or response.status_code == HTTPStatus.CREATED
        )
        ret = response

        if need_access_token:
            del headers["Authorization"]
            response = requests.request("GET", url, headers=headers, data=payload)
            assert response.status_code == HTTPStatus.UNAUTHORIZED

            headers["Authorization"] = Utils.get_random_token()
            response = requests.request("GET", url, headers=headers, data=payload)
            assert response.status_code == HTTPStatus.UNAUTHORIZED

        return ret


    def template_get_bad_request(url, headers, payload):
        response = requests.request("GET", url, headers=headers, data=payload)
        assert response.status_code == HTTPStatus.BAD_REQUEST

        return response


    def template_post(url, headers, payload, need_access_token=False):
        response = requests.request("POST", url, headers=headers, data=payload)
        assert (
            response.status_code == HTTPStatus.OK
            or response.status_code == HTTPStatus.CREATED
        )        
        ret = response

        if need_access_token:
            del headers["Authorization"]
            response = requests.request("POST", url, headers=headers, data=payload)
            
            assert response.status_code == HTTPStatus.UNAUTHORIZED

            headers["Authorization"] = Utils.get_random_token()
            response = requests.request("POST", url, headers=headers, data=payload)
            
            assert response.status_code == HTTPStatus.UNAUTHORIZED

        return ret


    def template_post_bad_request(url, headers, payload):
        response = requests.request("POST", url, headers=headers, data=payload)
        assert response.status_code == HTTPStatus.BAD_REQUEST

        return response


class Utils:

    @staticmethod
    def get_random_string(length):
        """
        Generates random string from ascii_lowercase set.
        ::length:: The length od the generated sequence. [int]
        """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))


    @staticmethod
    def get_random_token():
        """
        Generates random token with {TOKEN_LENGTH} length.
        This should be used as a dummy authentication token
        """
        TOKEN_LENGTH = 256
        return Utils.get_random_string(TOKEN_LENGTH)


    def replace_key_in_json(json, key, val):
        if isinstance(json, dict):
            for k, v in json.items():
                if k == key:
                    json[k] = val
                elif isinstance(v, list):
                    for i, item in enumerate(v):
                        v[i] = self.replace_key_in_json(item, key, val)
                elif isinstance(v, dict):
                    v = self.replace_key_in_json(v, key, val)
        return json


    def remove_key_from_json(input_dict, keys):
        if isinstance(input_dict, dict):
            return {
                k: self.remove_key_from_json(v, keys)
                for k, v in input_dict.items()
                if k not in keys
            }

        elif isinstance(input_dict, list):
            return [self.remove_key_from_json(element, keys) for element in input_dict]

        else:
            return input_dict
