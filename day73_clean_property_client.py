"""
Day 73 – REST API with requests: GET, POST, headers, error handling.
PCPP1 standard: type hints, docstrings, private attributes, PEP 8, British English.
"""

import requests
from requests import Response


class PropertyDataClient:
    """HTTP client for a property data REST API using requests.Session."""

    def __init__(self, base_url: str, api_key: str | None = None) -> None:
        """Initialise the client with a base URL and optional API key.

        Args:
            base_url: Root URL of the API (no trailing slash).
            api_key:  Optional bearer token for authenticated endpoints.
        """
        self._base_url: str = base_url.rstrip("/")
        self._session: requests.Session = requests.Session()
        if api_key:
            self._session.headers.update({"Authorization": f"Bearer {api_key}"})
        self._session.headers.update({"Content-Type": "application/json"})

    def _get(self, endpoint: str) -> Response:
        """Perform a GET request and raise on HTTP errors.

        Args:
            endpoint: Path appended to the base URL.

        Returns:
            Raw Response object.
        """
        url = f"{self._base_url}/{endpoint.lstrip('/')}"
        response = self._session.get(url, timeout=10)
        response.raise_for_status()
        return response

    def get_property(self, property_id: int) -> dict:
        """Retrieve a single property by ID.

        Args:
            property_id: Unique integer identifier.

        Returns:
            Property data as a dictionary.
        """
        return self._get(f"posts/{property_id}").json()

    def get_all_properties(self) -> list[dict]:
        """Retrieve all properties from the API.

        Returns:
            List of property dictionaries.
        """
        return self._get("posts").json()

    def post_deal(self, payload: dict) -> dict:
        """Submit a new deal via POST request.

        Args:
            payload: Dictionary of deal data to serialise as JSON.

        Returns:
            Created deal data as a dictionary.
        """
        url = f"{self._base_url}/posts"
        response = self._session.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()

    def delete_deal(self, deal_id: int) -> int:
        """Delete a deal by ID.

        Args:
            deal_id: Unique integer identifier of the deal.

        Returns:
            HTTP status code of the response.
        """
        url = f"{self._base_url}/posts/{deal_id}"
        response = self._session.delete(url, timeout=10)
        response.raise_for_status()
        return response.status_code

    def safe_get(self, endpoint: str) -> dict | None:
        """Perform a GET request, returning None on any request error.

        Args:
            endpoint: Path appended to the base URL.

        Returns:
            Parsed JSON dict or None if the request fails.
        """
        try:
            return self._get(endpoint).json()
        except requests.exceptions.RequestException:
            return None

    def __repr__(self) -> str:
        """Return an unambiguous string representation.

        Returns:
            Developer-facing string for this client instance.
        """
        return f"PropertyDataClient(base_url='{self._base_url}')"


if __name__ == "__main__":
    client = PropertyDataClient("https://jsonplaceholder.typicode.com")

    prop = client.get_property(1)
    print("Single property:", prop)

    all_props = client.get_all_properties()
    print(f"Total properties fetched: {len(all_props)}")

    new_deal = client.post_deal({"title": "Office acquisition", "body": "EC2 tower", "userId": 1})
    print("Posted deal:", new_deal)

    status = client.delete_deal(1)
    print("Delete status:", status)

    missing = client.safe_get("nonexistent/999")
    print("Safe get result:", missing)

    print(repr(client))