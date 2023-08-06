################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from __future__ import print_function
import pkg_resources
import re
import time
import requests
from ibm_ai_openscale.utils.client_errors import *


PAYLOAD_LOGGING_DETAILS_TYPE = u'payload_logging_type'
FUNCTION_DETAILS_TYPE = u'function_details_type'

UNKNOWN_ARRAY_TYPE = u'resource_type'
UNKNOWN_TYPE = u'unknown_type'

requests_session = requests.Session()


def is_ipython():
    # checks if the code is run in the notebook
    try:
        get_ipython
        return True
    except Exception:
        return False


def get_type_of_details(details):
    if 'resources' in details:
        return UNKNOWN_ARRAY_TYPE
    elif details is None:
        raise ClientError('Details doesn\'t exist.')
    else:
        try:
            if re.search(u'\/functions\/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return FUNCTION_DETAILS_TYPE
        except:
            pass

        try:
            if re.search(u'\/payload_logging\/[^\/]+$', details[u'metadata'][u'url']) is not None:
                return PAYLOAD_LOGGING_DETAILS_TYPE
        except:
            pass

        return UNKNOWN_TYPE


def docstring_parameter(args):
    def dec(obj):
        #obj.__doc__ = obj.__doc__.format(**args)
        return obj
    return dec


def version():
    try:
        version = pkg_resources.get_distribution("ibm-ai-openscale").version
    except pkg_resources.DistributionNotFound:
        version = u'0.0.1-local'

    return version


def install_package(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])

def install_package_from_pypi(name, version=None, test_pypi=False):
    from setuptools.command import easy_install

    if version is None:
        package_name = name
    else:
        package_name = "{}=={}".format(name, version)

    if test_pypi:
        index_part = ["--index-url", "https://test.pypi.org/simple/"]
    else:
        index_part = ["--index-url", "https://pypi.python.org/simple/"]

    easy_install.main(index_part + [package_name])

    import importlib
    globals()[name] = importlib.import_module(name)


def handle_response(expected_status_code, operationName, response, json_response=True):
    logger = logging.getLogger('handle_response')
    if response.status_code == expected_status_code:
        logger.info(u'Successfully finished {} for url: \'{}\''.format(operationName, response.url))
        logger.debug(u'Response({} {}): {}'.format(response.request.method, response.url, response.text))
        if json_response:
            try:
                return response.json()
            except Exception as e:
                raise ClientError(u'Failure during parsing json response: \'{}\''.format(response.text), e)
        else:
            return response.text
    else:
        raise ApiRequestFailure(u'Failure during {}.'.format(operationName), response)


def validate_enum(el, el_name, enum_class, mandatory=True):
    if mandatory and el is None:
        raise MissingValue(el_name)
    elif el is None:
        return

    if type(el) is not str or el not in enum_class.__dict__.values():
        raise UnexpectedType(el_name, enum_class, type(el))


def validate_type(el, el_name, expected_type, mandatory=True, subclass=False):
    if el_name is None:
        raise MissingValue(u'el_name')

    if type(el_name) is not str:
        raise UnexpectedType(u'el_name', str, type(el_name))

    if expected_type is None:
        raise MissingValue(u'expected_type')

    if type(expected_type) is not type and type(expected_type) is not list:
        raise UnexpectedType('expected_type', 'type or list', type(expected_type))

    if type(mandatory) is not bool:
        raise UnexpectedType(u'mandatory', bool, type(mandatory))

    if type(subclass) is not bool:
        raise UnexpectedType(u'subclass', bool, type(subclass))

    if mandatory and el is None:
        raise MissingValue(el_name)
    elif el is None:
        return

    validation_func = isinstance

    if subclass is True:
        validation_func = lambda x, y: issubclass(x.__class__, y)

    if type(expected_type) is list:
        try:
            next((x for x in expected_type if validation_func(el, x)))
            return True
        except StopIteration:
            return False
    else:
        if not validation_func(el, expected_type):
            raise UnexpectedType(el_name, expected_type, type(el))


def validate_meta_prop(meta_props, name, expected_type, mandatory=True):
    if name in meta_props:
        validate_type(meta_props[name], u'meta_props.' + name, expected_type, mandatory)
    else:
        if mandatory:
            raise MissingMetaProp(name)


def print_text_header_h1(title):
    print(u'\n\n' + (u'=' * (len(title) + 2)) + u'\n')
    print(' ' + title + ' ')
    print(u'\n' + (u'=' * (len(title) + 2)) + u'\n\n')


def print_text_header_h2(title):
    print(u'\n\n' + (u'-' * (len(title) + 2)))
    print(' ' + title + ' ')
    print((u'-' * (len(title) + 2)) + u'\n\n')


def print_synchronous_run(title, check_state, run_states=None, success_states=['success', 'finished'], failure_states=['failure', 'error', 'cancelled', 'canceled'], delay=5, get_result=None):
    if get_result is None:
        def tmp_get_result():
            if state in success_states:
                return 'Successfully finished.', None
            else:
                return 'Error occured.', None
        get_result = tmp_get_result

    print_text_header_h1(title)
    state = None

    while (run_states is not None and state in run_states) or (state not in success_states and state not in failure_states):
        last_state = state
        state = check_state()

        if state != last_state:
            print('\n' + state, end='')
        else:
            print('.', end='')

        time.sleep(delay)

    result_title, msg = get_result()

    print_text_header_h2(result_title)
    if msg is not None:
        print(msg)

    return state