from ibm_ai_openscale.utils import *
from ibm_ai_openscale.base_classes.configuration.table_viewer import TableViewer
from ibm_ai_openscale.base_classes.configuration.metrics_viewer import MetricsViewer
from ibm_ai_openscale.supporting_classes.enums import *


_DEFAULT_LIST_LENGTH = 50


class QualityMonitoring(TableViewer, MetricsViewer):
    """Manage fairness monitoring for asset."""
    def __init__(self, subscription, ai_client):
        TableViewer.__init__(self, ai_client, subscription, self, table_name='QualityMetrics',
                             conditions={'binding_id': subscription.binding_uid, 'subscription_id': subscription.uid})
        MetricsViewer.__init__(self, ai_client, subscription, MetricTypes.QUALITY_MONITORING)

    def enable(self, evaluation_method, threshold, min_records, spark_credentials=None, training_results_reference=None):
        """
        Enables model quality monitoring.

        :param evaluation_method: binary, multiclass or regression
        :type evaluation_method: str

        :param threshold: the threshold for quality metric (accuracy, areaUnderROC or r2).
        :type threshold: int

        :param min_records: minial feedback record count that triggers monitoring
        :type min_records: int

        :param spark_credentials: Spark service credentials needed for Spark models
        :type spark_credentials: dict

        """

        if evaluation_method is None or threshold is None or min_records is None:
            raise MissingValue('Missing one of required parameters: evaluation_method, threshold, min_records.')

        # TODO check if this is spark model == yes spark is required

        if spark_credentials is not None:
            params = {
                "evaluation_definition": {
                    "method": evaluation_method,
                    "threshold": threshold
                },
                "min_feedback_data_size": min_records,
                "secrets": {
                    "spark_instance": {
                        "credentials": spark_credentials,
                        "version": "2.1"
                    }
                }
            }
        elif training_results_reference is not None:
            params = {
                "evaluation_definition": {
                    "method": evaluation_method,
                    "threshold": threshold
                },
                "min_feedback_data_size": min_records,
                "secrets": {
                    "training_results_reference": training_results_reference
                },
                "execution": {
                    "compute_configuration": {
                        "name": "k80",
                    }
                },
            }
        else:
            raise MissingValue('Missing one of required parameters: spark_credentials or training_results_reference')

        response = requests_session.put(
            self._ai_client._href_definitions.get_quality_monitoring_href(self._subscription.uid),
            json={
                "enabled": True,
                "parameters": params
            },
            headers=self._ai_client._get_headers()
        )

        handle_response(200, u'quality monitoring setup', response)

    def get_details(self):
        """
        Returns details of quality monitoring configuration.

        :return: configuration of quality monitoring
        :rtype: dict
        """
        response = requests_session.get(
            self._ai_client._href_definitions.get_quality_monitoring_href(self._subscription.uid),
            headers=self._ai_client._get_headers()
        )

        return handle_response(200, u'quality monitoring configuration', response)

    def disable(self):
        """
        Disables quality monitoring.
        """

        response = requests_session.put(
            self._ai_client._href_definitions.get_quality_monitoring_href(self._subscription.uid),
            json={
                "enabled": False
            },
            headers=self._ai_client._get_headers()
        )

        handle_response(200, u'quality monitoring unset', response)

    def get_deployment_metrics(self, deployment_uid=None):
        """
        Get last quality metrics for deployment(s).

        :param deployment_uid: UID of deployment for which the metrics which be prepared (optional)
        :type deployment_uid: str

        :return: metrics
        :rtype: dict
        """
        self._subscription.get_deployment_metrics(deployment_uid=deployment_uid, metric_type=MetricTypes.QUALITY_MONITORING)

    def get_metrics(self, deployment_uid):
        """
        Returns quality monitoring metrics.

        :param deployment_uid: deployment uid for which the metrics will be retrieved
        :type deployment_uid: str

        :return: metrics for deployment
        :rtype: dict
        """
        return super(QualityMonitoring, self).get_metrics(deployment_uid)

    def show_table(self, limit=10):
        """
        Show records in quality metrics view. By default 10 records will be shown.

        :param limit: maximal number of fetched rows. By default set to 10. (optional)
        :type limit: int

        A way you might use me is:

        >>> subscription.quality_monitoring.show_table()
        >>> subscription.quality_monitoring.show_table(limit=20)
        >>> subscription.quality_monitoring.show_table(limit=None)
        """
        super(QualityMonitoring, self).show_table(limit=limit)

    def print_table_schema(self):
        """
        Show quality metrics view schema.
        """
        super(QualityMonitoring, self).print_table_schema()

    def get_table_content(self, format='pandas', limit=None):
        """
        Get content of quality metrics view in chosen format. By default the format is 'pandas'.

        :param format: format of returned content, may be one of following: ['python', 'pandas'], by default is set 'pandas'
        :type format: {str_type}

        :param limit: maximal number of fetched rows. (optional)
        :type limit: int

        A way you might use me is:

        >>> pandas_table_content = subscription.quality_monitoring.get_table_content()
        >>> table_content = subscription.quality_monitoring.get_table_content(format='python')
        >>> pandas_table_content = subscription.quality_monitoring.get_table_content(format='pandas')
        """
        return super(QualityMonitoring, self).get_table_content(format=format, limit=limit)

    def describe_table(self):
        """
        Describe the content of quality metrics view (pandas style). It will remove columns with unhashable values.

        :return: description/summary
        :rtype: DataFrame

        A way you might use me is:

        >>> subscription.quality_metrics.describe_table()
        >>> description = subscription.quality_metrics.describe_table()
        """
        super(QualityMonitoring, self).describe_table()