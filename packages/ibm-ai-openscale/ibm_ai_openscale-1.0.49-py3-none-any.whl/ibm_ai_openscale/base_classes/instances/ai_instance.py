from .instance import Instance
from ibm_ai_openscale.utils import *


class AIInstance(Instance):
    def __init__(self, source_uid, credentials, service_type):
        Instance.__init__(self, source_uid, credentials)
        validate_type(service_type, "service_type", str, True)

        self._service_type = service_type