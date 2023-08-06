import requests
from ibm_ai_openscale.base_classes.clients import Client
from ibm_ai_openscale.base_classes.configuration import *
from ibm_ai_openscale.base_classes import *


# TODO add when explainability will be added
# :var explainability: object managing explainability for this subscription
# :vartype explainability: Explainability

class Subscription:
    """
    Describes subscription in AI OpenScale

    :var uid: uid of subscription
    :vartype uid: str
    :var url: url of subscription
    :vartype url: str
    :var source_uid: uid of asset
    :vartype source_uid: str
    :var source_url: url of asset
    :vartype source_url: str
    :var binding_uid: uid of binding containing this subscription
    :vartype binding_uid: str
    :var payload_logging: object managing payload logging for this subscription
    :vartype payload_logging: PayloadLogging
    :var fairness_monitoring: object managing fairness monitoring for this subscription
    :vartype fairness_monitoring: FairnessMonitoring
    :var performance_monitoring: object managing performance monitoring for this subscription
    :vartype performance_monitoring: PerformanceMonitoring
    :var quality_monitoring: object managing quality monitoring for this subscription
    :vartype quality_monitoring: QualityMonitoring
    :var feedback_logging: object managing feedback logging for this subscription
    :vartype feedback_monitoring: FeedbackLogging
    """
    def __init__(self, uid, url, source_uid, source_url, client, ai_client):
        validate_type(uid, "uid", str, True)
        validate_type(source_uid, "source_uid", str, True)
        validate_type(client, "client", Client, True, subclass=True)

        self.uid = uid
        self.url = url
        self.source_uid = source_uid
        self.source_url = source_url
        self.binding_uid = client.binding_uid

        from ibm_ai_openscale.engines.generic_machine_learning.generic_client import GenericClient
        if type(client) is not GenericClient:
            self._engine_client = client._client
        else:
            self._engine_client = None

        self._ai_client = ai_client
        self._binding_client = client
        self.payload_logging = PayloadLogging(self, ai_client)
        self.fairness_monitoring = FairnessMonitoring(self, ai_client)
        self._explainability = Explainability(self, ai_client)
        self.performance_monitoring = PerformanceMonitoring(self, ai_client)
        self.quality_monitoring = QualityMonitoring(self, ai_client)
        self.feedback_logging = FeedbackLogging(self, ai_client)

    def get_details(self):
        """
        Get subscription details.

        :return: subscription details
        :rtype: dict
        """
        response = requests.get(
            self._ai_client._href_definitions.get_subscription_href(self.uid),
            headers=self._ai_client._get_headers()
        )

        return handle_response(200, 'getting subscription details', response, True)

    def get_deployment_uids(self):
        """
        Get deployment uids for this subscription.

        :return: deployment uids
        :rtype: list of str
        """
        deployments_details = self.get_details()['entity']['deployments']
        return [d['deployment_id'] for d in deployments_details]

    def list_deployments(self):
        """
        List deployment for this subscription.
        """
        deployments_details = self.get_details()['entity']['deployments']

        records = [[c['deployment_id'], c['name'], c['created_at'], c['deployment_type']] for c in deployments_details]
        table = Table(['uid', 'name', 'created', 'type'], records)
        table.list(title="Deployments for subscription with uid={}".format(self.uid))

    def get_deployment_metrics(self, deployment_uid=None, metric_type=None):
        """
        Get subscription last metrics for deployments.

        :param deployment_uid: UID of deployment for which the metrics which be prepared (optional)
        :type deployment_uid: str

        :param metric_type: metric type which should be returned (optional)
        :type metric_type: str

        :return: subscription metrics
        :rtype: dict
        """
        return self._ai_client.data_mart.get_deployment_metrics(subscription_uid=self.uid, deployment_uid=deployment_uid,
                                                                metric_type=metric_type)

    def update(self, add_all_deployments=True, deployment_uids=None):
        """
        Refresh deployments for this subscription. If deployment_uids list will be passed, the missing uids on the list will be removed from deployment monitoring.

        :param add_all_deployments: if set to True all deployments will be added
        :type add_all_deployments: bool

        :param deployment_uids: list of deployment uids to add (optional)
        :type deployment_uids: list of str
        """
        artifact = self._binding_client.get_artifact(self.source_uid)

        if deployment_uids is not None or add_all_deployments:
            deployments = self._binding_client.get_deployments(artifact, deployment_uids)

            current_deployment_uids = self.get_deployment_uids()

            for deployment in deployments:
                if deployment.guid not in current_deployment_uids:
                    response = requests.put(
                        self._ai_client._href_definitions.get_deployment_href(self.uid, deployment.guid),
                        json=deployment._to_json(),
                        headers=self._ai_client._get_headers()
                    )

                    handle_response(200, 'adding deployment monitoring', response)
                    print('Monitoring of deployment with uid={} successfully added.'.format(deployment.guid))
                else:
                    current_deployment_uids.remove(deployment.guid)

            for uid in current_deployment_uids:
                response = requests.delete(
                    self._ai_client._href_definitions.get_deployment_href(self.uid, uid),
                    headers=self._ai_client._get_headers()
                )

                handle_response(200, 'removing deployment monitoring', response)
                print('Monitoring of deployment with uid={} successfully removed.'.format(uid))