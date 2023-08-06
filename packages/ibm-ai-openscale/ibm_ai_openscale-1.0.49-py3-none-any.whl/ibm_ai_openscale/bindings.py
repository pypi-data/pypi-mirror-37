from ibm_ai_openscale.base_classes import Table
from ibm_ai_openscale.base_classes.instances import AIInstance
from ibm_ai_openscale.utils import *
from ibm_ai_openscale.engines.generic_machine_learning.generic_client import GenericClient


class Bindings:
    """
    Manage bindings of machine learning services.
    """
    def __init__(self, ai_client):
        from ibm_ai_openscale import APIClient
        validate_type(ai_client, "ai_client", APIClient, True)

        self._logger = logging.getLogger(__name__)
        self._ai_client = ai_client

    def add(self, name, instance):
        """
            Add binding.

            :param name: name of binding
            :type name: str

            :param instance: service instance type with authentication information (dict)
            :type instance: object

            :return: binding uid
            :rtype: str

            A way you might use me is:

            >>> client.bindings.add("my wml instance", WatsonMachineLearningInstance(credentials))
        """
        validate_type(name, "name", str, True)
        validate_type(instance, "instance", AIInstance, True, subclass=True)

        response = requests_session.post(
            self._ai_client._href_definitions.get_service_bindings_href(),
            json={
                "name": name,
                "service_type": instance._service_type,
                "instance_id": instance.source_uid,
                "credentials": instance.credentials
            },
            headers=self._ai_client._get_headers()
        )

        details = handle_response(201, 'bind instance', response, True)

        return details['metadata']['guid']

    def list(self, **kwargs):
        """
             List bindings.

             A way you might use me is:

             >>> client.data_mart.bindings.list()
             >>> client.data_mart.bindings.list(name='my binding')
             >>> client.data_mart.bindings.list(service_type='watson_machine_learning')
         """

        records = [[c['metadata']['guid'], c['entity']['name'], c['entity']['service_type'],
                    c['metadata']['created_at']] for c in self.get_details()['service_bindings']]
        table = Table(['uid', 'name', 'service_type', 'created'], records)
        table.list(filter_setup=kwargs, title="Service bindings")

    def delete(self, binding_uid, force=True):
        """
             Delete binding.

             :param binding_uid: uid of managed binding
             :type binding_uid: str

             :param force: force unbinding
             :type force: bool

             A way you might use me is:

             >>> client.data_mart.bindings.delete(binding_uid)
         """
        validate_type(binding_uid, "binding_uid", str, True)
        validate_type(force, "force", bool, True)

        response = requests_session.delete(
            self._ai_client._href_definitions.get_service_binding_href(binding_uid) + '?force=' + str(force).lower(),
            headers=self._ai_client._get_headers()
        )

        handle_response(202, 'unbinding of instance', response, False)

    def get_details(self, binding_uid=None):
        """
              Get details of managed binding(s).

              :param binding_uid: uid of managed binding (optional)
              :type binding_uid: str

              A way you might use me is:

              >>> client.data_mart.bindings.get_details(binding_uid)
              >>> client.data_mart.bindings.get_details()
        """
        validate_type(binding_uid, "binding_uid", str, False)

        if binding_uid is None:
            response = requests_session.get(
                self._ai_client._href_definitions.get_service_bindings_href(),
                headers=self._ai_client._get_headers()
            )

            return handle_response(200, 'getting bindings details', response, True)
        else:
            response = requests_session.get(
                self._ai_client._href_definitions.get_service_binding_href(binding_uid),
                headers=self._ai_client._get_headers()
            )

            return handle_response(200, 'getting binding details', response, True)

    def get_uids(self):
        """
              Get uids of managed bindings.

              A way you might use me is:

              >>> client.data_mart.bindings.get_uids()
        """
        return [binding['metadata']['guid'] for binding in self.get_details()['service_bindings']]

    def list_assets(self, **kwargs):
        """
              List available assets. Available assets are these assets which wasn't added yet as AI subscription:

              >>> client.data_mart.subscriptions.add(asset_uid) # adding asset to your AI Openscale instance

              A way you might use me is:

              >>> client.data_mart.bindings.list_assets()
              >>> client.data_mart.bindings.list_assets(source_uid='123')
        """
        records = [[c['source_uid'], c['name'], c['created'], c['type'],
                    ','.join([f['name'] + '-' + f['version'] for f in c['frameworks']]), c['binding_uid'],
                    c['subscription_uid'] if 'subscription_uid' in c else '-'] for c in self.get_asset_details()]
        table = Table(['source_uid', 'name', 'created', 'type', 'frameworks', 'binding_uid', 'subscription_uid'], records)
        table.list(filter_setup=kwargs, title="Available assets")

    def get_asset_details(self):
        """
              Get details of available assets (models and functions). Available assets are these assets which wasn't added yet as AI subscription:

              >>> client.data_mart.subscriptions.add(WatsonMachineLearningAsset(asset_uid)) # adding asset to your AI Openscale instance

              A way you might use me is:

              >>> client.data_mart.bindings.get_asset_details()
        """
        clients = self._ai_client._clients_manager.get_all().values()

        mapping = {s['entity']['asset']['asset_id']: s['metadata']['guid'] for s in self._ai_client.data_mart.subscriptions.get_details()['subscriptions']}

        assets = [{**asset.to_json(), **({'subscription_uid': mapping[asset.source_uid]} if asset.source_uid in mapping else {})} for client in clients for asset in client.get_artifacts()]

        return assets

    def get_asset_uids(self):
        """
              Get uids of available assets.

              A way you might use me is:

              >>> client.data_mart.bindings.get_asset_uids()
        """
        return [asset['source_uid'] for asset in self.get_asset_details()]

    def get_native_engine_client(self, binding_uid):
        """
        Returns native client for engine instance added to AIOS.

        :param binding_uid: UID of binding for which the client should be obtained
        :type: str

        :return: native client for particular binding
        :rtype: specific for particular engine, e.g for wml it will be WatsonMachineLearningAPIClient
        """
        client = self._ai_client._clients_manager.get_client(binding_uid)
        if type(client) is GenericClient:
            raise ClientError('Getting native client for generic instance is not possible.')
        else:
            return client._client

