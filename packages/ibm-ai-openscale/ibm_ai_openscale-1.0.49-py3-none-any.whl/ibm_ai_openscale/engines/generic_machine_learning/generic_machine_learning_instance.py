from ibm_ai_openscale.base_classes.instances import AIInstance
import uuid
from .generic_consts import GenericConsts


class GenericMachineLearningInstance(AIInstance):
    """
    Describes generic machine learning instance.

    :param source_uid: source uid of instance (optional)
    :type source_uid: str
    :param credentials: credentials to instance (optional)
    :type credentials: dict
    """
    def __init__(self, source_uid=None, credentials=None):
        AIInstance.__init__(
            self,
            'generic_instance_id_' + str(uuid.uuid4()) if source_uid is None else source_uid,
            {} if credentials is None else credentials,
            GenericConsts.SERVICE_TYPE
        )