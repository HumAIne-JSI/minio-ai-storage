import requests

class HumaineAuth:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.token = None

    def login(self, username, password):
        url = f"{self.base_url}/auth/login"
        response = requests.post(url, json={"username": username, "password": password})
        response.raise_for_status()
        self.token = response.json()["access_token"]
        return self.token

    def headers(self):
        if not self.token:
            raise ValueError("Not authenticated")
        return {"Authorization": f"Bearer {self.token}"}
