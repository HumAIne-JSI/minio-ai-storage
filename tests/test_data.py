import pytest
from minio_humaine_client.data import upload_data, download_data
from minio_humaine_client.auth import HumaineAuth

from unittest.mock import patch, mock_open

import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

HUMAINE_API_BASE_URL = os.getenv("HUMAINE_API_BASE_URL", "http://localhost:8000")
HUMAINE_API_TIMEOUT = int(os.getenv("HUMAINE_TIMEOUT", 30))
HUMAINE_API_USERNAME = os.getenv("HUMAINE_API_USERNAME", "user")
HUMAINE_API_PASSWORD = os.getenv("HUMAINE_API_PASSWORD", "pass")

@pytest.fixture
def mock_auth():
    auth = HumaineAuth(HUMAINE_API_BASE_URL)
    auth.token = "fake-token"
    return auth

def test_upload_data(mock_auth):
    with patch("builtins.open", mock_open(read_data=b"fake-data")):
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"result": "success"}

            result = upload_data(mock_auth, "dummy.csv")
            assert result["result"] == "success"

def test_download_data(mock_auth, tmp_path):
    file_path = tmp_path / "output.csv"
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"downloaded content"

        download_data(mock_auth, "object-key", file_path)
        assert file_path.read_bytes() == b"downloaded content"
