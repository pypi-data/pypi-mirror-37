
from xvector.api_config import ApiConfig
from xvector.utils.api_key_util import ApiKeyUtil
import requests
import os
import pandas as pd


def get_data_list(**kwargs):
    ApiKeyUtil().init_api_key_from_args(url="xdata", **kwargs)
    headers = ApiConfig.get_headers()
    url = ApiConfig.get_url()
    r = requests.get(url, headers=headers)
    print(r.request.headers, r.request.url)
    response = []
    items = r.json()
    if r.status_code == 200 and items and len(items) > 0:
        for item in items:
            obj = dict()
            obj["id"] = item["id"]
            obj["name"] = item["name"]
            response.append(obj)
        return response
    else:
        return r

def get_metadata(id, **kwargs):
    params = os.path.join("xdata", id, "metadata")
    ApiKeyUtil().init_api_key_from_args(url=params, **kwargs)
    headers = ApiConfig.get_headers()
    url = ApiConfig.get_url()
    r = requests.get(url, headers=headers)
    response = r.json()
    return response


def get_table(id, **kwargs):
    params = os.path.join("xdata", id, "dataframe")
    ApiKeyUtil().init_api_key_from_args(url=params, **kwargs)
    headers = ApiConfig.get_headers()
    url = ApiConfig.get_url()
    content = {}
    r = requests.post(url, headers=headers, json=content)
    response = r.json()
    result = {}
    if r.status_code==200:
        if 'column_schema' in response and 'rows' in response:
            df = pd.DataFrame(response["rows"], columns=[item['name'] for item in response["column_schema"]])
            print(df.count())
            result['df'] = df
        if "df_stats" in response:
            result["df_stats"] = response["df_stats"]
    return result
