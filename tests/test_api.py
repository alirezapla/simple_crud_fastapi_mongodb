import pytest
import httpx
import json

# from backend.exception import ApiError


class ApiError(Exception):
    pass


class ApiError(Exception):
    pass


URL = "http://0.0.0.0:8080/"


class TestCase:
    @pytest.fixture
    def _get_token(self):
        url = f"{URL}admin/login"
        payload = json.dumps({"username": "abbas@boazar.com", "password": "1"})
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        response = httpx.post(url, headers=headers, data=payload)
        try:
            return response.json()
        except:
            raise ApiError(response)

    def test_add_user(self, _get_token):
        url = f"{URL}user/"
        token = _get_token["access_token"]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        payload = {
            "first_name": "John1",
            "last_name": "Doe",
            "email": "jdoe@x.edu.ww",
            "national_id": "0011223355",
            "password": "1Ass_word",
        }
        response = httpx.post(url, headers=headers, data=json.dumps(payload))
        print(response.json())
        assert response.json()["message"] == "User added successfully."

    def test_get_user(self, _get_token):
        url = f"{URL}user/"
        token = _get_token["access_token"]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        response = httpx.get(url, headers=headers)
        assert response.json()["message"] == "Users data retrieved successfully"
        for user in response.json()["data"][0]:
            assert len(user["national_id"]) == 10
