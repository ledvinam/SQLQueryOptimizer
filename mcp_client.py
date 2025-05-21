import requests

class MCPClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    def get_schema(self, database):
        url = f"{self.base_url}/schema/{database}"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def execute_sql(self, database, sql):
        url = f"{self.base_url}/execute/{database}"
        resp = requests.post(url, json={"sql": sql}, headers=self.headers)
        resp.raise_for_status()
        return resp.json()
