import pytest
import requests
from http import HTTPStatus
import json

from utils import Utils, HTTPClient
from config import (
    payload_client_account,
    HEALTH_URL
)


@pytest.fixture(autouse=True)
def run_before_tests():
    pass


def test_health():
    payload = {}
    headers = {}

    response = requests.request("GET",
                                url=HEALTH_URL,
                                headers=headers,
                                data=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Healthy"