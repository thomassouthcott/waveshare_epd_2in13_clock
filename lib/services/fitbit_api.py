"""Class for Fitbit Service."""
from base64 import b64encode
from datetime import datetime
from hashlib import sha256
import logging
import requests
from secrets import token_hex
import time
from urllib.parse import urlencode

import requests.utils

from config import get_fitbit_config
from lib.services.api import APIService

logger = logging.getLogger()

class FitbitService(APIService):
    """Dataclass for API services."""
    def __init__(self):
        super().__init__(get_fitbit_config().api_key, get_fitbit_config().api_urls, get_fitbit_config().api_refresh_interval)

    def generate_code_challenge(self):
        """Generates a code verifier and challenge for the authorization."""
        return b64encode(sha256(get_fitbit_config().code_verifier.encode()).digest()).decode().replace("=", "").replace("+", "-").replace("/", "_")

    def _request(self):
        #START CHECKING VARIOUS API CONFIG ITEMS
        if get_fitbit_config().api_key == "":
            #Let's generate a authorization url for the user to visit
            logger.warning("[FITBIT] No API key found for Fitbit")
            logger.warning("[FITBIT] Please visit the following URL to authorize the application:")
            logger.warning(self.get_authorization_url())
            return None
        if get_fitbit_config().api_access_token == "":
            logger.debug("[FITBIT] No access token found for Fitbit")
            logger.debug("[FITBIT] Attempting to login to Fitbit")
            response = requests.post(self.get_login_url(self.get_login_params(get_fitbit_config().api_key)), headers={"Content-type":"application/x-www-form-urlencoded"}, timeout=10)
            json = response.json()
            if "error" in json:
                logger.error("[FITBIT] %s", json["error"])
                return None
            self.set_tokens(json)
        access_token = self.get_access_token()
        if access_token is None:
            logger.error("[FITBIT] Could not get access token")
            return None
        date = datetime.now().strftime("%Y-%m-%d")
        response = requests.get(get_fitbit_config().api_urls[2] + date + ".json", headers=self.get_request_headers(access_token), timeout=10)
        json = response.json()
        # Check if the API returned an error
        if not response.ok:
            logger.error("[FITBIT] %s", json)
            return None
        logger.debug("[FITBIT] Successfully retrieved data from Fitbit")
        logger.debug("[FITBIT] %i, %s", response.status_code, response.json())
        return json
    
    def set_tokens(self, json):
        """Sets the access token and refresh token in config."""
        expiry = time.time() + float(json["expires_in"])
        get_fitbit_config().set_tokens(json["access_token"], json["refresh_token"], expiry, json["user_id"])

    def get_request_headers(self, access_token):
        """Returns the request headers for the API."""
        return {"Authorization": f"Bearer {access_token}"}
    
    def get_authorization_url(self):
        """Returns the authorization URL for the API."""
        return get_fitbit_config().api_urls[0] + "?" + self.get_authorization_params()
    
    def get_authorization_params(self):
        """Returns the authorization URL for the API."""
        CODE_CHALLENGE_METHOD = "S256"
        RESONSE_TYPE = "code"
        code_challenge = self.generate_code_challenge()
        params = dict()
        params["client_id"] = get_fitbit_config().api_client_id
        params["response_type"] = RESONSE_TYPE
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = CODE_CHALLENGE_METHOD
        params["scope"] = get_fitbit_config().scope
        return urlencode(params)
    
    def get_login_params(self, code):
        """Returns the login URL for the API."""
        params = dict()
        params["client_id"] = get_fitbit_config().api_client_id
        params["grant_type"] = "authorization_code"
        params["code"] = code
        params["code_verifier"] = get_fitbit_config().code_verifier
        return params
    
    def get_refresh_body(self):
        """Returns the refresh URL for the API."""
        params = dict()
        params["grant_type"] = "refresh_token"
        params["refresh_token"] = get_fitbit_config().api_refresh_token
        params["client_id"] = get_fitbit_config().api_client_id
        return params

    def get_login_url(self, params = None):
        """Login to the API."""
        if params is None:
            return get_fitbit_config().api_urls[1]
        return get_fitbit_config().api_urls[1] + "?" + urlencode(params)
    
    def get_access_token(self):
        """Returns the access token for the API."""
        if time.time() > get_fitbit_config().api_expiry - 60:
            logger.debug("[FITBIT] Access token has expired. Refreshing.")
            response = requests.post(self.get_login_url(), headers={"Content-type":"application/x-www-form-urlencoded"}, data=self.get_refresh_body(), timeout=10)
            json = response.json()
            if not response.ok or "error" in json:
                logger.error("[FITBIT] %s", json)
                return None
            self.set_tokens(json)
        return get_fitbit_config().api_access_token

