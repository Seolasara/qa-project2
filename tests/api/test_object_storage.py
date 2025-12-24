import pytest
import requests
from src.config import config_reader as config


def test_OS004_entire_object_storage_list(api_headers):

    url = f"{config.base_url}/api/user/resource/storage/object_storage?count=50"

    response = requests.get(url, headers=api_headers)
    assert response.status_code == 200