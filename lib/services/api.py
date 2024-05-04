"""Dataclass for API services"""
import time

class APIService:
    """Dataclass for API services."""
    def __init__(self, api_key, api_urls, api_refresh_interval):
        self.api_key = api_key
        self.api_urls = api_urls
        self.api_refresh_interval = api_refresh_interval
        self.api_last_refresh = None

    def get_data(self):
        """Returns the data from the API."""
        if self.api_last_refresh is None:
            self.api_last_refresh = time.time()
            return self._request()
        if time.time() - self.api_last_refresh < self.api_refresh_interval:
            return None
        self.api_last_refresh = time.time()
        return self._request()

    def _request(self):
        pass
        
