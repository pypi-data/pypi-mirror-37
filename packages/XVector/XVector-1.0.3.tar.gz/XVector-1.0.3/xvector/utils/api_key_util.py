from xvector.api_config import ApiConfig
class ApiKeyUtil(object):
    @staticmethod
    def init_api_key_from_args(**kwargs):
        # set values
        if "base_url" in kwargs and kwargs["base_url"] is not None:
            ApiConfig.set_api_base(kwargs["base_url"])
        if "version" in kwargs and kwargs["version"] is not None:
            ApiConfig.set_version(kwargs["version"])
        if "api_key" in kwargs and kwargs["api_key"] is not None:
            ApiConfig.set_api_key(kwargs["api_key"])
        if "auth_token" in kwargs and kwargs["auth_token"] is not None:
            ApiConfig.set_auth_token(kwargs["auth_token"])
        if "url" in kwargs and kwargs["url"] is not None:
            ApiConfig.set_url(kwargs["url"])
        if "rows" in kwargs and kwargs["rows"] is not None:
            p = 1
            if "page" in kwargs and kwargs["page"] is not None:
                p = kwargs["page"]
            url = ApiConfig.url+"?p="+str(p)+"&n="+str(kwargs["rows"])
            ApiConfig.set_url(url)
        return True
