# src/dsp2_client/core/session.py

import httpx
import logging
from typing import Optional, Dict
from dsp2_client.config import settings

class DSP2Session:
    """
    Secure and robust HTTP session handler for the DSP2 API.

    - Handles OAuth2 (password grant) authentication.
    - Injects the Bearer token for every authenticated request.
    - Automatically re-authenticates on 401 (token expiration).
    - Configurable scopes, timeout, client_id, and client_secret.
    - Usable as a context manager to ensure proper resource cleanup.
    - Built-in structured logging for full auditability.
    """

    def __init__(
        self,
        username: str,
        password: str,
        scope: str = "stet ob",
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        log_level: Optional[str] = None,
    ):
        """
        Initialize the DSP2Session.

        Args:
            username (str): API username.
            password (str): API password.
            scope (str): Scopes required for API access.
            client_id (Optional[str]): Client ID if required.
            client_secret (Optional[str]): Client secret if required.
            base_url (Optional[str]): Base URL for the API.
            timeout (Optional[float]): Request timeout in seconds.
            log_level (Optional[str]): Log level (e.g., "INFO", "DEBUG").
        """
        self.username = username
        self.password = password
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url or settings.base_url
        self.timeout = timeout or settings.timeout

        # Setup logger
        self.logger = logging.getLogger("dsp2_client.session")
        self.logger.setLevel(log_level or settings.log_level)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self._client: Optional[httpx.Client] = None
        self._access_token: Optional[str] = None

    def __enter__(self):
        """
        Enter the context manager, opening the HTTP client.
        """
        self._client = httpx.Client(base_url=self.base_url, timeout=self.timeout)
        self.logger.debug("HTTP client opened (base_url=%s, timeout=%s)", self.base_url, self.timeout)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager, closing the HTTP client.
        """
        if self._client:
            self._client.close()
            self.logger.debug("HTTP client closed.")

    def authenticate(self):
        """
        Authenticate and retrieve a Bearer token.
        """
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "scope": self.scope,
        }
        if self.client_id:
            data["client_id"] = self.client_id
        if self.client_secret:
            data["client_secret"] = self.client_secret

        self.logger.info("Authenticating user %s...", self.username)
        response = self._client.post(
            "/oauth/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        res = response.json()
        self._access_token = res.get("access_token")
        if not self._access_token:
            self.logger.error("Authentication failed, missing token: %s", res)
            raise RuntimeError(f"Authentication failed, missing token: {res}")
        self.logger.debug("Authenticated successfully.")

    def _headers(self, extra: Optional[Dict] = None) -> Dict:
        """
        Build authentication headers. Automatically triggers authentication if not already done.

        Returns:
            dict: HTTP headers including Authorization.
        """
        if not self._access_token:
            self.authenticate()
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
        }
        if extra:
            headers.update(extra)
        return headers

    def get(self, path: str, **kwargs) -> httpx.Response:
        """
        Perform an authenticated GET request. Handles token expiration and auto-retry.

        Args:
            path (str): API route (absolute, starting with /).
            **kwargs: Additional arguments to httpx.Client.get.

        Returns:
            httpx.Response: HTTP response object.
        """
        try:
            response = self._client.get(path, headers=self._headers(), **kwargs)
            if response.status_code == 401:
                self.logger.warning("Token expired, re-authenticating...")
                self.authenticate()
                response = self._client.get(path, headers=self._headers(), **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as exc:
            self.logger.error("HTTP error on GET %s: %s", path, exc)
            raise

    def post(self, path: str, data=None, json=None, **kwargs) -> httpx.Response:
        """
        Perform an authenticated POST request. Handles token expiration and auto-retry.

        Args:
            path (str): API route (absolute, starting with /).
            data: Form data payload.
            json: JSON payload.
            **kwargs: Additional arguments to httpx.Client.post.

        Returns:
            httpx.Response: HTTP response object.
        """
        try:
            response = self._client.post(path, headers=self._headers(), data=data, json=json, **kwargs)
            if response.status_code == 401:
                self.logger.warning("Token expired, re-authenticating...")
                self.authenticate()
                response = self._client.post(path, headers=self._headers(), data=data, json=json, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as exc:
            self.logger.error("HTTP error on POST %s: %s", path, exc)
            raise

# Use this class as a context manager to ensure all HTTP connections are properly closed:
#
# with DSP2Session(username, password) as session:
#     response = session.get("/stet/identity")
#     print(response.json())
