import os
import requests
import pandas as pd
from xvector.XRequest import XRequest
from xvector.DataSet import DataSet


class XVectorArgumentException(Exception):
    pass


class XVector:
    auth_token = None

    def __init__(self, auth_token=None):

        if not auth_token:
            auth_token = os.environ.get('XVECTOR_AUTH_TOKEN')
            if not auth_token:
                raise XVectorArgumentException(
                    "auth_token is not present, please pass it to constructor or set XVECTOR_AUTH_TOKEN environment variable")
        self.auth_token = auth_token
        XRequest.set_auth_token(auth_token=auth_token)

    def get_dataset_list(self):
        return DataSet.get_all_datasets()
