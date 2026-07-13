import requests


class GoogleMapsClient:
    """
    Client for communicating with the Google Maps Scraper Engine.
    """

    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url

    def health(self):
        """
        Check whether the engine is running.
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/jobs",
                timeout=5
            )

            return response.status_code == 200

        except Exception:
            return False