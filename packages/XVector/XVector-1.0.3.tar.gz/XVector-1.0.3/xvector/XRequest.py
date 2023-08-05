import requests


class XRequestException(Exception):
    pass


class XRequest:
    base_url = 'https://xui.xvectorlabs.com/xserver'
    auth_token = None

    def __init__(self):
        pass

    @staticmethod
    def _get_sub_url(url):
        if url.find('/') == 0:
            return url.split('/', 1)[1]
        return url

    @staticmethod
    def set_auth_token(auth_token):
        XRequest.auth_token = auth_token

    @staticmethod
    def get_auth_token():
        if not XRequest.auth_token:
            raise XRequestException("Auth token not set")
        return XRequest.auth_token

    @staticmethod
    def _get_headers():
        return {'X-XVECTOR-API-KEY': XRequest.get_auth_token()}

    @staticmethod
    def form_url(sub_url):
        return '{base_url}/{sub_url}'.format(base_url=XRequest.base_url, sub_url=XRequest._get_sub_url(sub_url))

    @staticmethod
    def get(url):
        r = requests.get(XRequest.form_url(url), headers=XRequest._get_headers())
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            raise XRequestException('Authentication Error, please check the auth token')
        elif r.status_code == 403:
            raise XRequestException('Authorization Error, you cannot access this resource')
        else:
            raise XRequestException(r.text)
