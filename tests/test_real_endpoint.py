import pytest
from minio_humaine_client.auth import HumaineAuth

import requests
from requests.exceptions import HTTPError
from unittest.mock import patch

import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

HUMAINE_API_BASE_URL = os.getenv("HUMAINE_API_BASE_URL", "http://localhost:8000")
HUMAINE_API_TIMEOUT = int(os.getenv("HUMAINE_TIMEOUT", 30))
HUMAINE_API_USERNAME = os.getenv("HUMAINE_API_USERNAME", "user")
HUMAINE_API_PASSWORD = os.getenv("HUMAINE_API_PASSWORD", "pass")

def test_real_login_success():
    auth = HumaineAuth(HUMAINE_API_BASE_URL)
    assert HUMAINE_API_BASE_URL == "https://humaine-minio-api.euprojects.net"

    url = f"{HUMAINE_API_BASE_URL}/auth/auth"

    auth.login(HUMAINE_API_USERNAME, HUMAINE_API_PASSWORD)


    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "username": HUMAINE_API_USERNAME,
        "password": HUMAINE_API_PASSWORD
    }

    assert url == "https://humaine-minio-api.euprojects.net/auth/auth"

    response = requests.post(url, headers=headers, data=data)

    assert response.status_code == 200
    assert auth.token != ""

def test_real_upload():
    pass

