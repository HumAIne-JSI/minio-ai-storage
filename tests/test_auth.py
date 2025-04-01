import pytest
from minio_humaine_client.auth import HumaineAuth
from minio_humaine_client.config import DEFAULT_BASE_URL

import requests
from requests.exceptions import HTTPError
from unittest.mock import patch

def test_login_success():
    auth = HumaineAuth(DEFAULT_BASE_URL)
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access_token": "test-token"}

        token = auth.login("user", "pass")

        assert token == "test-token"
        assert auth.token == "test-token"
        assert auth.headers() == {"Authorization": "Bearer test-token"}

def test_login_failure():
    auth = HumaineAuth(DEFAULT_BASE_URL)
    with patch("requests.post") as mock_post:
        mock_post.return_value.raise_for_status.side_effect = HTTPError("401 Client Error")

        with pytest.raises(HTTPError):
            auth.login("wronguser", "wrongpass")
