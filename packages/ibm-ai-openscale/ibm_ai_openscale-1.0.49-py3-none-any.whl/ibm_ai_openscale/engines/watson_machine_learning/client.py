from ibm_ai_openscale.base_classes.clients import KnownServiceClient
from ibm_ai_openscale.base_classes import Artifact, SourceDeployment, Framework
from watson_machine_learning_client import WatsonMachineLearningAPIClient
from .consts import WMLConsts


class WMLClient(KnownServiceClient):
    service_type = WMLConsts.SERVICE_TYPE

    def __init__(self, binding_uid, service_credentials, project_id=None):
        KnownServiceClient.__init__(self, binding_uid)
        self._client = WatsonMachineLearningAPIClient(service_credentials, project_id)

    def _make_artifact_from_details(self, details):
        asset_type = 'function' if 'functions' in details['metadata']['url'] else 'model'

        if asset_type == 'model':
            frameworks = [Framework(details['entity']['model_type'].split('-')[0], details['entity']['model_type'].split('-')[1])]
        else:
            frameworks = []

        return Artifact(
            details['metadata']['guid'],
            details['metadata']['url'],
            self.binding_uid,
            details['entity']['name'],
            asset_type,
            details['metadata']['created_at'],
            frameworks,
            details
        )

    def get_artifact(self, source_uid):
        asset_details = self._client.repository.get_details(source_uid)
        return self._make_artifact_from_details(asset_details)

    def get_artifacts(self):
        models = self._client.repository.get_model_details()['resources']
        try:
            import logging
            logging.getLogger('watson_machine_learning_client.wml_client_error').disabled = True
            functions = self._client.repository.get_function_details()['resources']
        except:
            functions = []
        finally:
            import logging
            logging.getLogger('watson_machine_learning_client.wml_client_error').disabled = False

        return [self._make_artifact_from_details(asset) for asset in models + functions]

    def get_deployments(self, asset, deployment_uids=None):
        deployments = self._client.deployments.get_details()['resources']
        deployments = list(filter(lambda d: d['entity']['deployable_asset']['guid'] == asset.source_uid, deployments))

        if deployment_uids is not None:
            deployments = list(filter(lambda d: d['metadata']['guid'] in deployment_uids, deployments))

        return [
            SourceDeployment(
                deployment['metadata']['guid'],
                deployment['metadata']['url'],
                deployment['entity']['name'],
                deployment['entity']['type'],
                deployment['metadata']['created_at']
            ) for deployment in deployments
        ]
