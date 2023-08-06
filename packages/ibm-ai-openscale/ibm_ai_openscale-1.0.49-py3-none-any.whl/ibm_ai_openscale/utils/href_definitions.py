################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

TOKEN_ENDPOINT_HREF_PATTERN = u'{}/identity/token'

DATA_MART_HREF_PATTERN = u'{}/v1/data_marts/{}'
SERVICE_BINDINGS_HREF_PATTERN = u'{}/v1/data_marts/{}/service_bindings'
SERVICE_BINDING_HREF_PATTERN = u'{}/v1/data_marts/{}/service_bindings/{}'
SUBSCRIPTIONS_HREF_PATTERN = u'{}/v1/data_marts/{}/subscriptions'
SUBSCRIPTION_HREF_PATTERN = u'{}/v1/data_marts/{}/subscriptions/{}'
CONFIGURATION_HREF_PATTERN = u'{}/v1/data_marts/{}/subscriptions/{}/configurations/{}'
DEPLOYMENT_HREF_PATTERN = u'{}/v1/data_marts/{}/subscriptions/{}/deployments/{}'
PAYLOAD_STORING_HREF_PATTERN = u'{}/v1/data_marts/{}/scoring_payloads'
FAIRNESS_CONFIGURATION_PATTERN = u'{}/v1/fairness_monitoring'
FAIRNESS_RUNS_PATTERN = u'{}/v1/fairness_monitoring/{}/runs'


METRICS_HREF = u'{}/v1/data_marts/{}/metrics?format={}&metric_type={}&start={}&end={}&binding_id={}&subscription_id={}&deployment_id={}'
DEPLOYMENT_METRICS_HREF = u'{}/v1/data_marts/{}/deployment_metrics'

MODEL_EXPLANATION_CONFIGURATION_HREF = u'{}/v1/model_explanation_configurations/{}?data_mart_id={}&service_binding_id={}'
MODEL_EXPLANATION_CONFIGURATIONS_HREF = u'{}/v1/model_explanation_configurations'
MODEL_EXPLANATION_HREF = u'{}/v1/model_explanations/{}?data_mart_id={}'
MODEL_EXPLANATIONS_HREF = u'{}/v1/model_explanations'


class AIHrefDefinitions():
    def __init__(self, service_credentials):
        self._service_credentials = service_credentials
        self._iam_host = 'https://iam.bluemix.net'\
            if 'stage1' not in service_credentials['url']\
            else 'https://iam.stage1.bluemix.net' # TODO better condition

    def get_token_endpoint_href(self):
        return TOKEN_ENDPOINT_HREF_PATTERN.format(self._iam_host)

    def get_data_mart_href(self):
        return DATA_MART_HREF_PATTERN.format(self._service_credentials['url'], self._service_credentials['data_mart_id'])

    def get_service_bindings_href(self):
        return SERVICE_BINDINGS_HREF_PATTERN.format(self._service_credentials['url'], self._service_credentials['data_mart_id'])

    def get_service_binding_href(self, binding_uid):
        return SERVICE_BINDING_HREF_PATTERN.format(self._service_credentials['url'], self._service_credentials['data_mart_id'], binding_uid)

    def get_subscriptions_href(self):
        return SUBSCRIPTIONS_HREF_PATTERN.format(self._service_credentials['url'], self._service_credentials['data_mart_id'])

    def get_subscription_href(self, subscription_uid):
        return SUBSCRIPTION_HREF_PATTERN.format(self._service_credentials['url'], self._service_credentials['data_mart_id'], subscription_uid)

    def get_deployment_href(self, subscription_uid, deployment_uid):
        return DEPLOYMENT_HREF_PATTERN.format(self._service_credentials['url'], self._service_credentials['data_mart_id'], subscription_uid, deployment_uid)

    def get_payload_logging_href(self, subscription_uid):
        return CONFIGURATION_HREF_PATTERN.format(self._service_credentials['url'], self._service_credentials['data_mart_id'], subscription_uid, 'payload_logging')

    def get_payload_logging_storage_href(self):
        return PAYLOAD_STORING_HREF_PATTERN.format(self._service_credentials['url'], self._service_credentials['data_mart_id'])

    def get_fairness_monitoring_href(self, subscription_uid):
        return CONFIGURATION_HREF_PATTERN.format(self._service_credentials['url'], self._service_credentials['data_mart_id'], subscription_uid, 'fairness_monitoring')

    def get_fairness_monitoring_configuration_href(self):
        return FAIRNESS_CONFIGURATION_PATTERN.format(self._service_credentials['url'])

    def get_fairness_monitoring_runs_href(self, asset_id):
        return FAIRNESS_RUNS_PATTERN.format(self._service_credentials['url'], asset_id)

    def get_quality_monitoring_href(self, subscription_uid):
        return CONFIGURATION_HREF_PATTERN.format(self._service_credentials['url'], self._service_credentials['data_mart_id'], subscription_uid, 'quality_monitoring')

    def get_performance_monitoring_href(self, subscription_uid):
        return CONFIGURATION_HREF_PATTERN.format(self._service_credentials['url'], self._service_credentials['data_mart_id'], subscription_uid, 'performance_monitoring')

    def get_explainability_href(self, subscription_uid):
        return CONFIGURATION_HREF_PATTERN.format(self._service_credentials['url'], self._service_credentials['data_mart_id'], subscription_uid, 'explainability')

    def get_model_explanation_configurations_href(self):
        return MODEL_EXPLANATION_CONFIGURATIONS_HREF.format(self._service_credentials['url'])

    def get_model_explanation_configuration_href(self, model_uid, binding_uid):
        return MODEL_EXPLANATION_CONFIGURATION_HREF.format(self._service_credentials['url'], model_uid, self._service_credentials['data_mart_id'], binding_uid)

    def get_model_explanations_href(self):
        return MODEL_EXPLANATIONS_HREF.format(self._service_credentials['url'])

    def get_model_explanation_href(self, request_id):
        return MODEL_EXPLANATION_HREF.format(self._service_credentials['url'], request_id, self._service_credentials['data_mart_id'])

    def get_metrics_href(self, result_format, metric_type, start, end, binding_id, subscription_id, deployment_id):
        return METRICS_HREF.format(self._service_credentials['url'], self._service_credentials['data_mart_id'],
                                   result_format, metric_type, start, end, binding_id, subscription_id, deployment_id)

    def get_deployment_metrics_href(self):
        return DEPLOYMENT_METRICS_HREF.format(self._service_credentials['url'], self._service_credentials['data_mart_id'])
