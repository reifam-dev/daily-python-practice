# This file contains 3 deliberate bugs. Find and fix them.
import requests


class PropertyDataClient:

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
        self._session = requests.Session()

    def get_property(self, property_id: int) -> dict:
        url = f"{self._base_url}/properties/{property_id}"
        response = self._session.get(url, timeout=10)
        response.raise_for_status
        return response.json()                  # Bug 1: raise_for_status not called (missing parentheses)

    def post_deal(self, payload: dict) -> dict:
        url = f"{self._base_url}/deals"
        response = self._session.post(url, data=payload, timeout=10)  # Bug 2: data= should be json=
        response.raise_for_status()
        return response.json()

    def get_all_properties(self) -> list:
        url = f"{self._base_url}/properties"
        response = self._session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def delete_deal(self, deal_id: int) -> int:
        url = f"{self._base_url}/deals/{deal_id}"
        response = self._session.delete(url, timeout=10)
        response.raise_for_status()
        return response.status_code

    def safe_get(self, endpoint: str) -> dict | None:
        try:
            url = f"{self._base_url}/{endpoint}"
            response = self._session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:   # Bug 3: should catch RequestException not just ConnectionError
            return None


if __name__ == "__main__":
    client = PropertyDataClient("https://jsonplaceholder.typicode.com")
    result = client.safe_get("posts/1")
    print(result)