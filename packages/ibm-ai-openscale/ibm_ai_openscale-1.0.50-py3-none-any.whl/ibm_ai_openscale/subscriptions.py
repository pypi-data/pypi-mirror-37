from ibm_ai_openscale.base_classes import RefreshingTable
from ibm_ai_openscale.utils import *
from ibm_ai_openscale.supporting_classes import *
from ibm_ai_openscale.base_classes.assets import Asset, KnownServiceAsset
from ibm_ai_openscale.engines.generic_machine_learning import GenericAsset
from ibm_ai_openscale.engines.generic_machine_learning.generic_client import GenericClient


class Subscriptions:
    def __init__(self, ai_client):
        from ibm_ai_openscale import APIClient
        validate_type(ai_client, "ai_client", APIClient, True)
        self._ai_client = ai_client
        self._list_header = ['uid', 'name', 'type', 'binding_uid', 'source_uid', 'created']
        self._subscriptions_table = RefreshingTable(['uid', 'url', 'name', 'type', 'binding_uid', 'source_uid', 'source_url', 'created'], self._get_records)

    def _get_records(self):

        records = [
            [
                a['metadata']['guid'],
                a['metadata']['url'],
                a['entity']['asset']['name'],
                a['entity']['asset']['asset_type'],
                a['entity']['service_binding_id'],
                a['entity']['asset']['asset_id'],
                a['entity']['asset']['url'] if 'url' in a['entity']['asset'] else None,
                a['metadata']['created_at']
            ] for a in self.get_details()['subscriptions']
        ]


        return records # deployments?

    def get_details(self, subscription_uid=None):
        """
              Get details of managed asset(s).

              :param subscription_uid: uid of managed asset (optional)
              :type subscription_uid: str

              A way you might use me is:

              >>> client.data_mart.subscriptions.get_details(subscription_uid)
              >>> client.data_mart.subscriptions.get_details()
        """
        validate_type(subscription_uid, "subscription_uid", str, False)

        if subscription_uid is None:
            response = requests_session.get(
                self._ai_client._href_definitions.get_subscriptions_href(),
                headers=self._ai_client._get_headers()
            )

            return handle_response(200, 'getting subscriptions details', response, True)
        else:
            response = requests_session.get(
                self._ai_client._href_definitions.get_subscription_href(subscription_uid),
                headers=self._ai_client._get_headers()
            )

            return handle_response(200, 'getting subscription details', response, True)

    def get_uids(self):
        """
              Get uids of managed subscriptions.

              A way you might use me is:

              >>> client.data_mart.subscriptions.get_uids()
        """
        return [subscription['metadata']['guid'] for subscription in self.get_details()['subscriptions']]

    def list(self, **kwargs):
        """
              List managed assets.

              A way you might use me is:

              >>> client.data_mart.subscriptions.list()
        """
        self._subscriptions_table.list(filter_setup=kwargs, title="Subscriptions", column_list=self._list_header)

    def get(self, subscription_uid=None, choose=None, **kwargs):
        """
            Get object to managed subscriptions.

            :param subscription_uid: managed asset uid
            :type subscription_uid: str
            :param choose: strategy of choosing result if more than one, possible values:

                - None - if more than one exception will be thrown
                - 'random' - random one will be choosen
                - 'first' - first created will be choosen
                - 'last' - last created will be choosen
            :type choose: str
            :param kwargs: are used to determine result when asset_uid is unset

            :return: subscription object
            :rtype: Subscription

            A way you might use me is:

            >>> asset_1 = client.data_mart.subscriptions.get(subscription_uid)
            >>> asset_2 = client.data_mart.subscriptions.get(name='my test asset')
            >>> asset_3 = client.data_mart.subscriptions.get(name='my test asset', choose='last')
        """
        validate_type(subscription_uid, "subscription_uid", str, False)
        validate_type(choose, "choose", str, False)
        validate_enum(choose, "choose", Choose, False)

        constraints = kwargs

        if subscription_uid is not None:
            constraints['uid'] = subscription_uid

        record = self._subscriptions_table.get_record(choose, **constraints)
        binding_uid = record[self._subscriptions_table.header.index('binding_uid')]
        if subscription_uid is None:
            subscription_uid = record[self._subscriptions_table.header.index('uid')]

        subscription_url = record[self._subscriptions_table.header.index('url')]
        source_uid = record[self._subscriptions_table.header.index('source_uid')]
        source_url = record[self._subscriptions_table.header.index('source_url')]

        client = self._ai_client._clients_manager.get_client(binding_uid)
        return client.get_subscription(subscription_uid, subscription_url, source_uid, source_url, self._ai_client)

    def add(self, asset, add_all_deployments=True, deployment_uids=None):
        """
             Add asset (model or function) to managed subscriptions.

             :param asset: asset object
             :type asset: Asset
             :param add_all_deployments: if this will be set to True and deployments_uids will be set to None it will cause adding all deployments for this asset
             :type add_all_deployments: bool
             :param deployment_uids: list of deployment uids which should be added for this asset
             :type deployment_uids: list of string or None

             A way you might use me is:

             >>> subscription_1 = client.data_mart.subscriptions.add(model_uid) # all deployments will be added as by default add_all_deployments=True
             >>> subscription_2 = client.data_mart.subscriptions.add(function_uid) # all deployments will be added as by default add_all_deployments=True
             >>> subscription_3 = client.data_mart.subscriptions.add(function_uid, add_all_deployments=False) # no deployment uids will be added
             >>> subscription_4 = client.data_mart.subscriptions.add(function_uid, deployment_uids=['1224', '2345']) # only these two will be added
        """
        validate_type(asset, "asset", [GenericAsset, KnownServiceAsset], True, subclass=True) # TODO check if works

        # get client
        if asset.binding_uid is not None:
            client = self._ai_client._clients_manager.get_client(asset.binding_uid)
        elif isinstance(asset, KnownServiceAsset):
            clients = self._ai_client._clients_manager.get_all()
            key = list(filter(lambda key: clients[key].contains_source_uid(asset.source_uid), clients))[0]
            client = clients[key]
        elif type(asset) == GenericAsset:
            clients = self._ai_client._clients_manager.get_all()
            keys = list(filter(lambda key: type(clients[key]) is GenericClient, clients))
            if len(keys) > 1:
                raise ClientError('More than one GenericInstance added to AIOS instance. Set `binding_uid` parameter to indicate to which the asset should be bounded.')
            if len(keys) == 0:
                raise ClientError('No GenericInstances added to this AIOS instance.')
            client = clients[keys[0]]
        else:
            raise UnexpectedType('asset', [GenericAsset, KnownServiceAsset], asset.__class__)

        # use client to get artifact and deployments
        if type(asset) == GenericAsset:
            artifact = client.prepare_artifact(asset)
        else:
            artifact = client.get_artifact(asset.source_uid)

        if deployment_uids is None and not add_all_deployments:
            deployments = []
        else:
            deployments = client.get_deployments(asset, deployment_uids)

        # transform deployments to deployment records
        deployment_records = list(map(lambda d: {
            "deployment_id": d.guid,
            "url": d.url,
            "name": d.name,
            "deployment_type": d.deployment_type,
            "created_at": d.created
        }, deployments))

        # make call
        response = requests_session.post(
            self._ai_client._href_definitions.get_subscriptions_href(),
            json={
                "service_binding_id": artifact.binding_uid,
                "asset": {
                    "asset_id": artifact.source_uid,
                    "url": artifact.source_url,
                    "name": artifact.name,
                    "asset_type": artifact.type,
                    "created_at": artifact.created
                },
                "deployments": deployment_records
            },
            headers = self._ai_client._get_headers()
        )

        details = handle_response(201, 'subscription of asset', response, True)

        return self.get(details['metadata']['guid'])

    def delete(self, subscription_uid):
        """
              Unsubscribe asset.

              :param subscription_uid: managed asset uid
              :type subscription_uid: str

              A way you might use me is:

              >>> client.data_mart.subscriptions.delete(subscription_uid)
        """
        validate_type(subscription_uid, "subscription_uid", str, True)

        response = requests_session.delete(
            self._ai_client._href_definitions.get_subscription_href(subscription_uid),
            headers=self._ai_client._get_headers()
        )

        handle_response(202, 'deletion of asset', response, False)