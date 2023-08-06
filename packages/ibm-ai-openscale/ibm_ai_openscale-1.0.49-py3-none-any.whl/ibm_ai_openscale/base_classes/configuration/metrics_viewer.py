from datetime import datetime, timedelta
from ibm_ai_openscale.utils import *


class MetricsViewer():
    def __init__(self, ai_client, subscription, metric_type):
        self._ai_client = ai_client
        self._subscription = subscription
        self._metric_type = metric_type

    def get_metrics(self, deployment_uid):
        validate_type(deployment_uid, 'deployment_uid', str, True)
        subscription_details = self._subscription.get_details()

        start = datetime.strptime(subscription_details['metadata']['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ") -timedelta(hours=1)

        response = requests_session.get(
            self._ai_client._href_definitions.get_metrics_href(
                'samples',
                self._metric_type,
                start.isoformat() + 'Z',
                datetime.utcnow().isoformat() + 'Z',
                self._subscription.binding_uid,
                self._subscription.uid,
                deployment_uid
            ),
            headers=self._ai_client._get_headers()
        )

        return handle_response(200, "getting {} metrics".format(self._metric_type), response, True)