import uuid
import datetime
from ibm_ai_openscale.base_classes.clients import Client
from .generic_consts import GenericConsts
from ibm_ai_openscale.base_classes import Artifact, SourceDeployment
from ibm_ai_openscale.utils import *
from .generic_asset import GenericAsset


class GenericClient(Client):
    service_type = GenericConsts.SERVICE_TYPE

    def __init__(self, binding_uid, ai_client, project_id=None):
        Client.__init__(self, binding_uid)
        self._ai_client = ai_client

    def prepare_artifact(self, asset):
        validate_type(asset, 'asset', GenericAsset, True)

        return Artifact(
            asset.source_uid,
            asset.source_url,
            self.binding_uid,
            asset.name,
            asset.asset_type,
            str(datetime.datetime.now().isoformat() + 'Z'),
            asset.frameworks,
            asset.source_entry
        )

    def get_artifact(self, source_uid):
        asset = self._ai_client.data_mart.subscriptions.get_details(source_uid)

        return Artifact(
            asset['entity']['asset']['asset_id'],
            asset['entity']['asset']['url'],
            asset['entity']['service_binding_id'],
            asset['entity']['asset']['name'],
            asset['entity']['asset']['asset_type'],
            asset['entity']['asset']['created_at'],
            [],
            asset
        )

    def get_artifacts(self):
        assets = self._ai_client.data_mart.subscriptions.get_details()['subscriptions']

        return [Artifact(
            asset['entity']['asset']['asset_id'],
            asset['entity']['asset']['url'],
            asset['entity']['service_binding_id'],
            asset['entity']['asset']['name'],
            asset['entity']['asset']['asset_type'],
            asset['entity']['asset']['created_at'],
            [],
            asset
        ) for asset in assets if asset['entity']['service_binding_id'] == self.binding_uid]

    def get_deployments(self, asset, deployment_uids=None):
        if deployment_uids is not None:
            return [SourceDeployment(uid, None, 'Deployment with uid=' + uid, 'online', str(datetime.datetime.now().isoformat() + 'Z')) for uid in deployment_uids]
        else:
            uid = 'generic_deployment_uid_' + str(uuid.uuid4())
            print('Creating default deployment for generic asset with uid:', uid)
            return [SourceDeployment(uid, None, asset.name, 'online', str(datetime.datetime.now().isoformat() + 'Z'))]
