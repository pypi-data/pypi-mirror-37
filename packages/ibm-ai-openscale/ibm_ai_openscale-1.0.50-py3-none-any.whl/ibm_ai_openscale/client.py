################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

import json
import base64
from datetime import datetime, timedelta

from ibm_ai_openscale.data_mart import DataMart
from ibm_ai_openscale.utils import *
from ibm_ai_openscale.clients_manager import ClientsManager

'''
.. module:: APIClient
   :platform: Unix, Windows
   :synopsis: AI OpenScale API Client.

.. moduleauthor:: IBM
'''


class APIClient:
    """
    AI OpenScale client.

    :var data_mart: Manage db connection
    :vartype data_mart: DataMart
    :var version: Returns version of the python library.
    :vartype version: str
    """
    def __init__(self, aios_credentials):
        """
        :param aios_credentials: credentials to AI OpenScale instance
        """
        validate_type(aios_credentials, "aios_credentials", dict, True)
        if 'url' not in aios_credentials:
            raise MissingValue("aios_credentials.url")
        validate_type(aios_credentials['url'], "aios_credentials.url", str, True)
        if 'data_mart_id' not in aios_credentials:
            raise MissingValue("aios_credentials.data_mart_id")
        validate_type(aios_credentials['data_mart_id'], "aios_credentials.data_mart_id", str, True)
        if 'apikey' not in aios_credentials:
            raise MissingValue("aios_credentials.apikey")
        validate_type(aios_credentials['apikey'], "aios_credentials.apikey", str, True)

        self._logger = logging.getLogger(__name__)
        self._service_credentials = aios_credentials
        self.version = version()
        self._href_definitions = AIHrefDefinitions(aios_credentials)
        self._token = self._create_token()

        self.data_mart = DataMart(self)
        self._clients_manager = ClientsManager(self.data_mart.bindings)
        self._logger.info(u'Client successfully initialized')

    def _get_headers(self, content_type='application/json', no_content_type=False):
        validate_type(content_type, "content_type", str, True)
        validate_type(no_content_type, "no_content_type", bool, True)

        headers = {
            'Authorization': 'Bearer ' + self._get_token(),
            #'X-AIOS-User-Client': 'PythonClient'
        }

        if not no_content_type:
            headers.update({'Content-Type': content_type})

        return headers

    def _get_token(self):
        if self._token is None:
            self._token = self._create_token()
        elif self._get_expiration_datetime() - timedelta(minutes=30) < datetime.now():
            self._refresh_token()

        return self._token

    def _create_token(self):
        response = requests_session.post(
            self._href_definitions.get_token_endpoint_href(),
            data={
                "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                "apikey": self._service_credentials['apikey']
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
        )
        if response.status_code == 200:
            token = response.json()['access_token']
            return token
        else:
            raise ApiRequestFailure(u'Error during getting IAM Token.', response)

    def _refresh_token(self):
        self._token = self._create_token()
        #
        # response = requests_session.put(
        #     self._href_definitions.get_token_endpoint_href(),
        #     json={'token': self._token},
        #     headers={
        #         'Content-Type': 'application/json',
        #         'Accept': 'application/json',
        #         'X-WML-User-Client': 'PythonClient'
        #     }
        # )
        #
        # if response.status_code == 200:
        #     self._token = response.json().get(u'token')
        # else:
        #     raise ApiRequestFailure(u'Error during refreshing ML Token.', response)

    def _get_expiration_datetime(self):
        token_parts = self._token.split('.')
        token_padded = token_parts[1] + '=' * (len(token_parts[1]) % 4)
        token_info = json.loads(base64.b64decode(token_padded).decode('utf-8'))
        token_expire = token_info.get('exp')

        return datetime.fromtimestamp(token_expire)