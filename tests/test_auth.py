import pytest
from minio_humaine_client.auth import HumaineAuth

import requests
from requests.exceptions import HTTPError
from unittest.mock import patch

import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

HUMAINE_API_BASE_URL = os.getenv("HUMAINE_API_BASE_URL", "http://localhost:8000")
HUMAINE_API_TIMEOUT = int(os.getenv("HUMAINE_TIMEOUT", 30))
HUMAINE_API_USERNAME = os.getenv("HUMAINE_API_USERNAME", "user")
HUMAINE_API_PASSWORD = os.getenv("HUMAINE_API_PASSWORD", "pass")

def test_login_success():
    auth = HumaineAuth(HUMAINE_API_BASE_URL)
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access_token": "test-token"}

        token = auth.login("user", "pass")

        assert token == "test-token"
        assert auth.token == "test-token"
        assert auth.headers() == {"Authorization": "Bearer test-token"}

def test_login_failure():
    auth = HumaineAuth(HUMAINE_API_BASE_URL)
    with patch("requests.post") as mock_post:
        mock_post.return_value.raise_for_status.side_effect = HTTPError("401 Client Error")

        with pytest.raises(HTTPError):
            auth.login("wronguser", "wrongpass")
