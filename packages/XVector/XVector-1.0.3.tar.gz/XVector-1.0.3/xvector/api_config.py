import os


class ApiConfig:

    api_base = 'http://xui.xvectorlabs.com/xserver'
    api_version = "api"
    auth_header = "X-XVECTOR-AUTH-TOKEN"
    auth_token = None
    api_key = None
    api_header = "X-XVECTOR-API-KEY"
    url = None

    @staticmethod
    def set_url(url):
        ApiConfig.url = url
        return ApiConfig.url

    @staticmethod
    def set_version(v):
        ApiConfig.api_version = v
        return ApiConfig.api_version

    @staticmethod
    def set_api_base(base_url):
        ApiConfig.api_base = base_url
        return ApiConfig.api_base

    @staticmethod
    def set_api_key(key):
        ApiConfig.api_key = key
        return ApiConfig.api_key

    @staticmethod
    def set_auth_token(token):
        ApiConfig.auth_token = token
        return ApiConfig.auth_token

    @staticmethod
    def get_headers():
        if ApiConfig.api_header is not None and ApiConfig.api_key is not None:
            return {ApiConfig.api_header: ApiConfig.api_key, 'Content-Type': 'application/json'}
        elif ApiConfig.auth_header is not None and ApiConfig.auth_token is not None:
            return {ApiConfig.auth_header: ApiConfig.auth_token, 'Content-Type': 'application/json'}
        else:
            raise ValueError("Invalid headers")

    @staticmethod
    def get_url():
        if ApiConfig.api_version is not None and ApiConfig.url is not None:
            return os.path.join(ApiConfig.api_base, ApiConfig.api_version, ApiConfig.url)
        else:
            raise ValueError("Invalid API Url")
