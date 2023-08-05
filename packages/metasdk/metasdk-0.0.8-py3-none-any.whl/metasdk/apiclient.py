import requests

from metasdk import read_developer_settings
from metasdk.exceptions import SDKError
from metasdk.internal import read_cfg, write_cfg

AUTH_CACHE_FILE = "/.rwmeta/auth_cache.json"
OAUTH_TOKEN_URL = "https://account.devision.io/oauth2/token"


class ApiClient:
    """
    Упрощает взаимодействие с внутренними API Devision
    """

    def __init__(self, host, api_version, access_token=None, refresh_token=None, client_id=None, client_secret=None):
        """
        :type app: metasdk.MetaApp
        """
        self.host = host
        self.api_version = api_version
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret

    def request(self, method_path, get_params=None, post_data=None):
        auth_cache = read_cfg(AUTH_CACHE_FILE)
        if auth_cache:
            if self.refresh_token == auth_cache.get('refresh_token', ''):
                self.access_token = auth_cache.get('access_token', '')

        if not self.access_token:
            self.refresh_access_token()

        if not self.access_token:
            raise ValueError("access_token должен был быть получен")

        for try_idx in range(2):
            url = self.host + '/' + self.api_version + '/' + method_path
            headers = {"Authorization": "Bearer " + self.access_token}

            req_param = {
                "method": "POST",
                "url": url,
                "data": get_params,
                "json": post_data,
                "headers": headers
            }
            resp = requests.request(**req_param)
            if resp.status_code == 401:
                self.refresh_access_token()
                continue

            return resp.json()

    def refresh_access_token(self):
        resp = requests.post(OAUTH_TOKEN_URL, data={
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        }, headers={
            "Content-Type": "application/x-www-form-urlencoded"
        })

        json = resp.json()
        if json.get('error'):
            raise SDKError(json)
        self.access_token = json.get('access_token')

        write_cfg(AUTH_CACHE_FILE, {
            "refresh_token": self.refresh_token,
            "access_token": self.access_token
        })

    @staticmethod
    def build_from_developer_settings(api_name: str, api_version: str):
        """
        :param api_name: Example hello
        :param api_version: Example v1, v2alpha
        :return: ApiClient
        """
        developer_settings = read_developer_settings()

        api_host = "http://" + api_name + ".apis.devision.io"
        return ApiClient(
            host=api_host,
            api_version=api_version,
            access_token=None,
            refresh_token=developer_settings['refreshToken'],
            client_id=developer_settings['clientId'],
            client_secret=developer_settings['clientSecret'],
        )
