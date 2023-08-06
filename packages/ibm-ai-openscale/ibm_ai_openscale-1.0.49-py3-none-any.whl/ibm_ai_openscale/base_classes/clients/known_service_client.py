from .client import Client
from ibm_ai_openscale.utils import *


class KnownServiceClient(Client):
    def __init__(self, binding_uid):
        Client.__init__(self, binding_uid)