from ibm_ai_openscale.utils import *
from ibm_ai_openscale.supporting_classes import *
from ibm_ai_openscale.subscriptions import Subscriptions
from ibm_ai_openscale.bindings import Bindings


class DataMart:
    """
    Manages DB Instance.

    :var bindings: Manage bindings of you AI OpenScale instance.
    :vartype bindings: Bindings
    :var subscriptions: Manage subscriptions of you AI OpenScale instance.
    :vartype subscriptions: Subscriptions
    """
    def __init__(self, ai_client):
        from ibm_ai_openscale.client import APIClient
        validate_type(ai_client, 'ai_client', APIClient, True)
        self._ai_client = ai_client
        self.bindings = Bindings(ai_client)
        self.subscriptions = Subscriptions(ai_client)

    def setup(self, postgres_credentials, schema=None):
        """
        Setups db instance.

        :param postgres_credentials: describes the instance which should be connected
        :type postgres_credentials: dict

        :param schema: schema in your database under which the tables should be created (optional)
        :type schema: str
        """
        validate_type(postgres_credentials, 'postgres_credentials', dict, True)
        validate_type(postgres_credentials['uri'], 'postgres_credentials.uri', str, True)

        payload = {
            "database_type": "postgresql",
            "credentials": postgres_credentials
        }

        if schema is not None:
            payload['location'] = {
                "schema": schema
            }

        response = requests_session.put(
            self._ai_client._href_definitions.get_data_mart_href(),
            json={"database_configuration": payload},
            headers=self._ai_client._get_headers()
        )

        handle_response(200, "setup of data mart", response, False)

    def get_details(self):
        """
        Get db instance details.

        :return: db instance details
        :rtype: dict
        """
        response = requests_session.get(
            self._ai_client._href_definitions.get_data_mart_href(),
            headers=self._ai_client._get_headers()
        )

        return handle_response(200, "getting data mart details", response, True)

    def get_deployment_metrics(self, subscription_uid=None, asset_uid=None, deployment_uid=None, metric_type=None):
        """
        Get metrics.

        :param subscription_uid: UID of subscription for which the metrics which be prepared (optional)
        :type subscription_uid: str

        :param asset_uid: UID of asset for which the metrics which be prepared (optional)
        :type asset_uid: str

        :param deployment_uid: UID of deployment for which the metrics which be prepared (optional)
        :type deployment_uid: str

        :param metric_type: metric type which should be returned (optional)
        :type metric_type: str

        :return: metrics
        :rtype: dict
        """
        validate_type(subscription_uid, 'subscription_uid', str, False)
        validate_type(asset_uid, 'asset_uid', str, False)
        validate_type(deployment_uid, 'deployment_uid', str, False)
        validate_enum(metric_type, 'metric_type', MetricTypes, False)

        response = requests_session.get(
            self._ai_client._href_definitions.get_deployment_metrics_href(),
            headers=self._ai_client._get_headers()
        )

        details = handle_response(200, "getting deployment metrics", response, True)['deployment_metrics']

        if subscription_uid is not None:
            details = list(filter(lambda x: x['subscription']['subscription_id'] == subscription_uid, details))

        if asset_uid is not None:
            details = list(filter(lambda x: x['asset']['asset_id'] == asset_uid, details))

        if deployment_uid is not None:
            details = list(filter(lambda x: x['deployment']['deployment_id'] == deployment_uid, details))

        if metric_type is not None:
            for record in details:
                record['metrics'] = list(filter(lambda m: m['metric_type'] == metric_type, record['metrics']))

        return {'deployment_metrics': details}

    def delete(self, force=True):
        """
        Delete data_mart configuration.

        :param force: force configuration deletion
        :type force: bool
        """
        validate_type(force, 'force', bool, True)
        response = requests_session.delete(
            self._ai_client._href_definitions.get_data_mart_href() + '?force=' + str(force).lower(),
            headers=self._ai_client._get_headers()
        )

        handle_response(202, "delete of data mart", response, False)
