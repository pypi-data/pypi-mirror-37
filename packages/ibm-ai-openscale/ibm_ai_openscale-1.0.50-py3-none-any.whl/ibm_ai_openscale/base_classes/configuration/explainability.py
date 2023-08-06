from ibm_ai_openscale.utils import *
from ibm_ai_openscale.supporting_classes import *
from ibm_ai_openscale.base_classes.configuration.table_viewer import TableViewer
from ibm_ai_openscale.supporting_classes.enums import *


_DEFAULT_LIST_LENGTH = 50


class Explainability(TableViewer):
    """Manage explainability for asset."""
    def __init__(self, subscription, ai_client):
        TableViewer.__init__(self, ai_client, subscription, self, subscription.binding_uid + '_explanation')
        self._ai_client = ai_client
        self._subscription = subscription

    def enable(self, model_type, model_data_type, label_column, feature_columns, training_data_reference, categorical_columns=None):
        """
        Enables explainability.

        :param model_type: model type
        :type model_type: str

        :param model_data_type: model data type
        :type model_data_type: str

        :param label_column: label column
        :type label_column: str

        :param feature_columns: feature columns
        :type feature_columns: list of str

        :param categorical_columns: categorical columns (optional)
        :type categorical_columns: list of str

        :param training_data_reference: training data reference
        :type training_data_reference: BluemixCloudObjectStorageReference

        """
        validate_type(model_type, 'model_type', str, True)
        validate_enum(model_type, 'model_type', ExplainabilityModelType, True)
        validate_type(model_data_type, 'model_data_type', str, True)
        validate_enum(model_data_type, 'model_data_type', ExplainabilityModelDataType, True)
        validate_type(label_column, 'label_column', str, True)
        validate_type(feature_columns, 'feature_columns', list, True)
        validate_type(training_data_reference, 'training_data_reference', [BluemixCloudObjectStorageReference], True, subclass=True)
        validate_type(categorical_columns, 'categorical_columns', list, False)

        try:
            self._subscription.payload_logging.enable()
        except:
            pass

        if type(training_data_reference) is BluemixCloudObjectStorageReference:
            training_data_reference_config = {
                "connection": {
                    "url": "https://s3.us-west.objectstorage.uat.softlayer.net",
                    "resource_instance_id": training_data_reference.credentials['resource_instance_id'],
                    "iam_url": "https://iam.stage1.ng.bluemix.net/oidc/token",
                    "api_key": training_data_reference.credentials['apikey']
                },
                "source": {
                    "file_name": training_data_reference.path.split('/')[-1],
                    "infer_schema": "1",
                    "file_format": training_data_reference.path.split('.')[-1],
                    "bucket": '/'.join(training_data_reference.path.split('/')[:-1]),
                    "type": "bluemixcloudobjectstorage"
                }
            }
        else:
            raise ClientError('Not supported training_data_reference type: {}'.format(type(training_data_reference)))

        params = {
            "model_type": model_type,
            "model_data_type": model_data_type,
            "model_source": "wml", # TODO maybe it should be detected?
            "label_column": label_column,
            "feature_columns": feature_columns,
            "training_data_reference": training_data_reference_config
        }

        if training_data_reference.first_line_header is not None:
            params['training_data_reference']['source']['firstlineheader'] = training_data_reference.first_line_header

        if categorical_columns is not None:
            params["categorical_columns"] = categorical_columns

        response = requests_session.post(
            self._ai_client._href_definitions.get_model_explanation_configurations_href(),
            json={
                "data_mart_id": self._ai_client._service_credentials['data_mart_id'],
                "service_binding_id": self._subscription.binding_uid,
                "model_id": self._subscription.source_uid,
                "parameters": params
                },
            headers=self._ai_client._get_headers()
        )

        handle_response(200, u'explainability setup', response)

    def get_details(self):
        """
        Will return details of explainability. Info about configuration.

        :return: configuration of explainability
        :rtype: dict
        """
        response = requests_session.get(
            self._ai_client._href_definitions.get_explainability_href(self._subscription.uid),
            headers=self._ai_client._get_headers()
        )

        return handle_response(200, u'explainability get details', response)

    def disable(self):
        """
        Disables explainability.
        """

        response = requests_session.put(
            self._ai_client._href_definitions.get_explainability_href(self._subscription.uid),
            json={
                "enabled": False
            },
            headers=self._ai_client._get_headers()
        )

        handle_response(200, u'explainability unset', response)

    def run(self, transaction_id):
        headers = self._ai_client._get_headers()
        headers['exp_user_id'] = 'xyz'

        response = requests_session.post(
            self._ai_client._href_definitions.get_model_explanations_href(),
            json={
                "transaction_id": transaction_id,
                "data_mart_id": self._ai_client._service_credentials['data_mart_id']
            },
            headers=headers
        )

        result = handle_response(200, u'explainability run', response, True)

        request_id = result['metadata']['request_id']

        def check_state():
            response = requests_session.get(
                self._ai_client._href_definitions.get_model_explanation_href(request_id),
                headers=headers
            )

            details = handle_response(200, u'explainability get details', response, True)

            return details['entity']['status']

        def get_result():
            response = requests_session.get(
                self._ai_client._href_definitions.get_model_explanation_href(request_id),
                headers=headers
            )

            details = handle_response(200, u'explainability get details', response, True)
            state = details['entity']['status']

            if state in ['success', 'finished']:
                return "Successfully finished run", "Result:\n" + details['entity']['predictions']
            else:
                return "Run failed with status: {}".format(state), 'Reason: {}'.format(details['entity']['error']['error_msg'])

        print_synchronous_run(
            'Looking for explanation for {}'.format(transaction_id),
            check_state,
            get_result=get_result
        )

    def show_table(self, limit=10):
        """
        Show records in explainability view. By default 10 records will be shown.

        :param limit: maximal number of fetched rows. By default set to 10. (optional)
        :type limit: int

        A way you might use me is:

        >>> subscription.explainability.show_table()
        >>> subscription.explainability.show_table(limit=20)
        >>> subscription.explainability.show_table(limit=None)
        """
        super(Explainability, self).show_table(limit=limit)

    def print_table_schema(self):
        """
        Show explainability view schema.
        """
        super(Explainability, self).print_table_schema()

    def get_table_content(self, format='pandas', limit=None):
        """
        Get content of explainability view in chosen format. By default the format is 'pandas'.

        :param format: format of returned content, may be one of following: ['python', 'pandas'], by default is set 'pandas'
        :type format: {str_type}

        :param limit: maximal number of fetched rows. (optional)
        :type limit: int

        A way you might use me is:

        >>> pandas_table_content = subscription.explainability.get_table_content()
        >>> table_content = subscription.explainability.get_table_content(format='python')
        >>> pandas_table_content = subscription.explainability.get_table_content(format='pandas')
        """
        return super(Explainability, self).get_table_content(format=format, limit=limit)

    def describe_table(self):
        """
        Describe the content of explainability view (pandas style).

        A way you might use me is:

        >>> pandas_table_content = subscription.explainability.describe_table()
        """
        super(Explainability, self).describe_table()




