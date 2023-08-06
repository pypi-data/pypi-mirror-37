from ibm_ai_openscale.utils import *


class Client:
    service_type = None

    def __init__(self, binding_uid):
        validate_type(binding_uid, "binding_uid", str, True)
        self.binding_uid = binding_uid

    def get_artifact(self, source_uid):
        raise NotImplemented()

    def get_artifacts(self):
        raise NotImplemented()

    def get_deployments(self, asset, deployment_uids=None):
        raise NotImplemented()

    def get_subscription(self, uid, url, source_uid, source_url, ai_client):
        from ibm_ai_openscale.base_classes.subscriptions import Subscription
        return Subscription(uid, url, source_uid, source_url, self, ai_client)

    def contains_source_uid(self, uid):
        validate_type(uid, "uid", str, True)

        uids = [x.source_uid for x in self.get_artifacts()]
        return uid in uids