"""Package skeleton

.. moduleauthor:: Wojciech Sobala <wojciech.sobala@pl.ibm.com>
"""

from .utils import version
from .client import APIClient

from watson_machine_learning_client.utils import is_python_2
if is_python_2():
    import logging
    logger = logging.getLogger('ibm_ai_openscale_initialization')
    logger.warning("Python 2 is not officially supported.")
