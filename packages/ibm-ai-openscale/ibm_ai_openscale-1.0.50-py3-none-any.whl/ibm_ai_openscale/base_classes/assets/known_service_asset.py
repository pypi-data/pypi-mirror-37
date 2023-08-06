from ibm_ai_openscale.base_classes.assets import Asset
from ibm_ai_openscale.utils import *


class KnownServiceAsset(Asset):
    def __init__(self, source_uid, binding_uid=None):
        validate_type(source_uid, 'source_uid', str, True)
        validate_type(binding_uid, 'binding_uid', str, False)
        Asset.__init__(self, binding_uid)
        self.source_uid = source_uid
