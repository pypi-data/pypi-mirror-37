from types import ModuleType
from ibm_ai_openscale.base_classes.clients import Client, KnownServiceClient
from ibm_ai_openscale.engines.generic_machine_learning.generic_client import GenericClient
from ibm_ai_openscale.engines.generic_machine_learning.generic_consts import GenericConsts
from .utils.client_errors import ClientError
from .utils import validate_type
from .bindings import Bindings


def find_client_classes(module_obj, max_depth=5):
    elements = []

    if max_depth < 0:
        return []

    for el in module_obj.__dict__.values():
        if type(el) is ModuleType:
            elements.extend(find_client_classes(el, max_depth-1))
        elif type(el) is type:
            if issubclass(el, Client) and el is not Client and el is not KnownServiceClient and el is not GenericClient:
                elements.append(el)

    return list(set(elements))

# these are classes against which instance type will be checked to create client object for this instance
_client_classes = find_client_classes(__import__('ibm_ai_openscale'))


class ClientsManager:
    def __init__(self, bindings):
        validate_type(bindings, "bindings", Bindings, True)

        self.clients = {}
        self.bindings = bindings

    def get_all(self):
        binding_uids = [c['metadata']['guid'] for c in self.bindings.get_details()['service_bindings']]

        for binding_uid in binding_uids:
            if binding_uid not in self.clients:
                self.get_client(binding_uid)

        return self.clients

    def get_client(self, binding_uid):
        validate_type(binding_uid, "binding_uid", str, True)

        if binding_uid in self.clients:
            return self.clients[binding_uid]

        details = self.bindings.get_details(binding_uid)

        if details['entity']['service_type'] == GenericConsts.SERVICE_TYPE:
            client = GenericClient(binding_uid, self.bindings._ai_client)
            self.clients[binding_uid] = client
            return client

        for client_class in _client_classes:
            if details['entity']['service_type'] == client_class.service_type:
                client = client_class(binding_uid, details['entity']['credentials'])
                self.clients[binding_uid] = client
                return client

        raise ClientError('Invalid service name. Cannot create specific client: {}'.format(details['entity']['service_type']))