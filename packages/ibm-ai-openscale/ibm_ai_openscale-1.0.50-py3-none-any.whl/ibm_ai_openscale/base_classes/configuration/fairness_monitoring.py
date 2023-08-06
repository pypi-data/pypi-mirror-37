from ibm_ai_openscale.utils import *
from ibm_ai_openscale.base_classes.configuration.table_viewer import TableViewer
from ibm_ai_openscale.base_classes.configuration.metrics_viewer import MetricsViewer
from ibm_ai_openscale.supporting_classes import *


_DEFAULT_LIST_LENGTH = 50


class FairnessMonitoring(TableViewer, MetricsViewer):
    """Manage fairness monitoring for asset."""
    def __init__(self, subscription, ai_client):
        TableViewer.__init__(self, ai_client, subscription, self, "FairnessMetrics",
                             conditions={'binding_id': subscription.binding_uid, 'subscription_id': subscription.uid})
        MetricsViewer.__init__(self, ai_client, subscription, MetricTypes.FAIRNESS_MONITORING)

    def enable(self, features, deployment_uid=None, prediction_column=None, favourable_classes=None, unfavourable_classes=None, min_records=None):
        """
        Enables fairness monitoring.

        :param features: the features for fairness monitoring
        :type features: list of features

        :param prediction_column: the name of column with predicted classes (optional)
        :type prediction_column: str

        :param favourable_classes: list of favourable classes (optional)
        :type favourable_classes: list of str

        :param unfavourable_classes: list of unfavourable classes (optional)
        :type unfavourable_classes: list of str

        :param min_records: minimal number of records (optional)
        :type min_records: int

        """
        validate_type(features, 'features', list, True)
        for feature in features:
            validate_type(feature, 'feature', Feature, True)
        validate_type(prediction_column, 'prediction_column', str, False)
        validate_type(favourable_classes, 'favourable_classes', [str, list], False)
        validate_type(unfavourable_classes, 'unfavourable_classes', [str, list], False)
        validate_type(min_records, 'min_records', int, False)

        if deployment_uid is None:
            uids = self._subscription.get_deployment_uids()
            if len(uids) == 0:
                raise ClientError('No deployments existing for subscription.')
            elif len(uids) > 1:
                raise ClientError('More than one deployments existing for subscription: {}'.format(uids))

            deployment_uid = uids[0]

        try:
            self._subscription.payload_logging.enable()
        except:
            pass

        params = {
            "features": [feature._to_json() for feature in features]
        }

        if prediction_column is not None:
            params["class_label"] = prediction_column

        if favourable_classes is not None:
            params["favourable_class"] = favourable_classes

        if unfavourable_classes is not None:
            params["unfavourable_class"] = unfavourable_classes

        if min_records is not None:
            params["min_records"] = min_records

        response = requests_session.post(
            self._ai_client._href_definitions.get_fairness_monitoring_configuration_href(),
            json={
                "data_mart_id": self._ai_client._service_credentials['data_mart_id'],
                "asset_id": self._subscription.uid,
                "deployment_id": deployment_uid,
                "parameters": params
            },
            headers=self._ai_client._get_headers()
        )

        handle_response(202, u'fairness monitoring setup', response)

    def get_details(self):
        """
        Returns details of fairness monitoring configuration.

        :return: configuration of fairness monitoring
        :rtype: dict
        """
        response = requests_session.get(
            self._ai_client._href_definitions.get_fairness_monitoring_href(self._subscription.uid),
            headers=self._ai_client._get_headers()
        )

        return handle_response(200, u'fairness monitoring configuration', response)

    def disable(self):
        """
        Disables fairness monitoring.
        """

        response = requests_session.put(
            self._ai_client._href_definitions.get_fairness_monitoring_href(self._subscription.uid),
            json={
                "enabled": False
            },
            headers=self._ai_client._get_headers()
        )

        handle_response(200, u'fairness monitoring unset', response)

    def get_deployment_metrics(self, deployment_uid=None):
        """
        Get last fairness metrics for deployment(s).

        :param deployment_uid: UID of deployment for which the metrics which be prepared (optional)
        :type deployment_uid: str

        :return: metrics
        :rtype: dict
        """
        self._subscription.get_deployment_metrics(deployment_uid=deployment_uid, metric_type=MetricTypes.FAIRNESS_MONITORING)

    def run(self, deployment_uid=None):
        if deployment_uid is None:
            uids = self._subscription.get_deployment_uids()
            if len(uids) == 0:
                raise ClientError('No deployments existing for subscription.')
            elif len(uids) > 1:
                raise ClientError('More than one deployments existing for subscription: {}'.format(uids))

            deployment_uid = uids[0]

        response = requests_session.post(
            self._ai_client._href_definitions.get_fairness_monitoring_runs_href(self._subscription.uid),
            json={
                "data_mart_id": self._ai_client._service_credentials['data_mart_id'],
                "deployment_id": deployment_uid,
                "subscription_id": self._subscription.uid
            },
            headers=self._ai_client._get_headers()
        )

        handle_response(202, u'fairness monitoring run', response)

    def get_metrics(self, deployment_uid):
        """
        Returns fairness monitoring metrics.

        :param deployment_uid: deployment uid for which the metrics will be retrieved
        :type deployment_uid: str

        :return: metrics for deployment
        :rtype: dict
        """
        return super(FairnessMonitoring, self).get_metrics(deployment_uid)

    def show_table(self, limit=10):
        """
        Show records in fairness metrics view. By default 10 records will be shown.

        :param limit: maximal number of fetched rows. By default set to 10. (optional)
        :type limit: int

        A way you might use me is:

        >>> subscription.fairness_monitoring.show_table()
        >>> subscription.fairness_monitoring.show_table(limit=20)
        >>> subscription.fairness_monitoring.show_table(limit=None)
        """
        super(FairnessMonitoring, self).show_table(limit=limit)

    def print_table_schema(self):
        """
        Show fairness metrics view schema.
        """
        super(FairnessMonitoring, self).print_table_schema()

    def get_table_content(self, format='pandas', limit=None):
        """
        Get content of fairness metrics view in chosen format. By default the format is 'pandas'.

        :param format: format of returned content, may be one of following: ['python', 'pandas'], by default is set 'pandas'
        :type format: {str_type}

        :param limit: maximal number of fetched rows. (optional)
        :type limit: int

        A way you might use me is:

        >>> pandas_table_content = subscription.fairness_monitoring.get_table_content()
        >>> table_content = subscription.fairness_monitoring.get_table_content(format='python')
        >>> pandas_table_content = subscription.fairness_monitoring.get_table_content(format='pandas')
        """
        return super(FairnessMonitoring, self).get_table_content(format=format, limit=limit)

    def describe_table(self):
        """
        Describe the content of fairness metrics view (pandas style). It will remove columns with unhashable values.

        :return: description/summary
        :rtype: DataFrame

        A way you might use me is:

        >>> subscription.fairness_metrics.describe_table()
        >>> description = subscription.fairness_metrics.describe_table()
        """
        super(FairnessMonitoring, self).describe_table()
