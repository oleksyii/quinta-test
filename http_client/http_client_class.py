import requests

class HttpClient:
    def __init__(self, api_key, base_url="https://api.clockify.me/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-Api-Key": api_key,
            "Content-Type": "application/json",
        })

    def get(self, endpoint, params=None) -> dict | None:
        """Perform a GET request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        self._handle_response(response)
        return response.json()

    def post(self, endpoint, data=None) -> dict | None:
        """Perform a POST request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=data)
        self._handle_response(response)
        return response.json()

    def put(self, endpoint, data=None) -> dict | None:
        """Perform a PUT request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, json=data)
        self._handle_response(response)
        return response.json()

    def delete(self, endpoint) -> dict | None:
        """Perform a DELETE request."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url)
        self._handle_response(response)
        return response.json()

    def _handle_response(self, response) -> dict | None:
        """Handle HTTP errors."""
        if not response.ok:
            print(f"Error: {response.status_code}, {response.text}")
            response.raise_for_status()