import datetime
import uuid
from ibm_ai_openscale.utils import *
from ibm_ai_openscale.base_classes.configuration.table_viewer import TableViewer


_DEFAULT_LIST_LENGTH = 50


class PayloadLogging(TableViewer):
    """Manage payload logging for asset."""
    def __init__(self, subscription, ai_client):
        TableViewer.__init__(self, ai_client, subscription, self)

    def enable(self, dynamic_schema_update=None):
        """
        Enables payload logging.

        :param dynamic_schema_update: schema will be automatically updated when asset will be scored (optional)
        :type dynamic_schema_update: bool
        """

        payload = {
            "enabled": True,
        }

        if dynamic_schema_update is not None:
            payload['parameters'] = {
                'dynamic_schema_update': dynamic_schema_update
            }

        response = requests_session.put(
            self._ai_client._href_definitions.get_payload_logging_href(self._subscription.uid),
            json=payload,
            headers=self._ai_client._get_headers()
        )

        handle_response(200, u'payload logging setup', response)

    def get_details(self):
        """
        Will return details of payload logging. Info about configuration.

        :return: configuration of payload logging
        :rtype: dict
        """
        response = requests_session.get(
            self._ai_client._href_definitions.get_payload_logging_href(self._subscription.uid),
            headers=self._ai_client._get_headers()
        )

        return handle_response(200, u'payload logging configuration', response)

    def disable(self):
        """
        Disables payload logging.
        """

        response = requests_session.put(
            self._ai_client._href_definitions.get_payload_logging_href(self._subscription.uid),
            json={
                "enabled": False
            },
            headers=self._ai_client._get_headers()
        )

        handle_response(200, u'payload logging unset', response)

    def store(self, request, response, scoring_id=None, scoring_timestamp=None, response_time=None, deployment_id=None):
        """
        Stores payload logging in payload logging table.

        :param request: scoring request
        :type request: dict

        :param response: scoring response
        :type response: dict

        :param scoring_id: scoring identifier (optional). If not provided random uid is assigned.
        :type scoring_id: str

        :param scoring_timestamp: scoring request timestamp (optional). If not provided current time is assigned.
        :type scoring_timestamp: str

        :param response_time: scoring response time in ms (optional)
        :type response: int

        :param deployment_id: deployment identifier (optional). If not provided first deployment id from subscription is taken.
        :type deployment_id: str

        """

        validate_type(request, "request", dict, True)
        validate_type(response, "response", dict, True)
        validate_type(scoring_id, "scoring_id", str, False)
        validate_type(deployment_id, "deployment_id", str, False)
        validate_type(scoring_timestamp, "scoring_timestamp", str, False)
        validate_type(response_time, "response_time", int, False)

        if deployment_id is not None:
            deployment_uid = deployment_id
        else:
            deployments = self._subscription.get_details()['entity']['deployments']
            if len(deployments) > 0:
                deployment_uid = deployments[0]['deployment_id']
            else:
                deployment_uid = 'generic_deployment'

        payload = {
                    "binding_id": self._subscription.binding_uid,
                    "subscription_id": self._subscription.uid,
                    "deployment_id": deployment_uid,
                    "request": request,
                    "response": response
        }

        if scoring_timestamp is not None:
            payload['scoring_timestamp'] = scoring_timestamp
        else:
            payload['scoring_timestamp'] = str(datetime.datetime.utcnow())

        if scoring_id is not None:
            payload['scoring_id'] = scoring_id
        else:
            payload['scoring_id'] = str(uuid.uuid4())

        if response_time is not None:
            payload['response_time'] = str(response_time)

        response = requests_session.post(
            self._ai_client._href_definitions.get_payload_logging_storage_href(),
            json=[payload],
            headers=self._ai_client._get_headers()
        )

        handle_response(202, u'payload logging storage', response)

    def show_table(self, limit=10):
        """
        Show records in payload logging table. By default 10 records will be shown.

        :param limit: maximal number of fetched rows. By default set to 10. (optional)
        :type limit: int

        A way you might use me is:

        >>> subscription.payload_logging.show_table()
        >>> subscription.payload_logging.show_table(limit=20)
        >>> subscription.payload_logging.show_table(limit=None)
        """
        super(PayloadLogging, self).show_table(limit=limit)

    def print_table_schema(self):
        """
        Show payload logging table schema.
        """
        super(PayloadLogging, self).print_table_schema()

    def get_table_content(self, format='pandas', limit=None):
        """
        Get content of payload logging table in chosen format. By default the format is 'pandas'.

        :param format: format of returned content, may be one of following: ['python', 'pandas'], by default is set 'pandas'
        :type format: {str_type}

        :param limit: maximal number of fetched rows. (optional)
        :type limit: int

        A way you might use me is:

        >>> pandas_table_content = subscription.payload_logging.get_table_content()
        >>> table_content = subscription.payload_logging.get_table_content(format='python')
        >>> pandas_table_content = subscription.payload_logging.get_table_content(format='pandas')
        """
        return super(PayloadLogging, self).get_table_content(format=format, limit=limit)

    def describe_table(self):
        """
        Describe the content of payload logging table (pandas style).

        A way you might use me is:

        >>> pandas_table_content = subscription.payload_logging.describe_table()
        """
        super(PayloadLogging, self).describe_table()
