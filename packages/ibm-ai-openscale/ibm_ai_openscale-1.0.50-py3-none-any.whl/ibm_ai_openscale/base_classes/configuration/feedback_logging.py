from ibm_ai_openscale.utils import *
from ibm_ai_openscale.base_classes.configuration.table_viewer import TableViewer


_DEFAULT_LIST_LENGTH = 50


class FeedbackLogging(TableViewer):
    """Manage payload logging for asset."""
    def __init__(self, subscription, ai_client):
        TableViewer.__init__(self, ai_client, subscription, subscription.quality_monitoring)
        self._schema = subscription._ai_client.data_mart.get_details()['database_configuration']['location']['schema']

    def _validate_if_table_accessible(self):
        quality_details = self._subscription.quality_monitoring.get_details()

        if 'table_name' not in quality_details['parameters']:
            raise ClientError('No information about table name. Table cannot be accessed.')

        tablename = quality_details['parameters']['table_name']

        if not tablename.startswith(self._schema + '.'):
            raise ClientError('Table is outside AIOS schema. It cannot be accessed.')

    def store(self, feedback_data, fields=None):
        """
            Send feedback data to learning system.

            :param feedback_data: rows of feedback data to be send
            :type feedback_data: list of rows
            :param fields: list of fields (optional)
            :type fields: list of strings

            A way you might use me is

            >>> subscription.feedback_logging.store([["a1", 1, 1.0], ["a2", 2, 3.4]])
            >>> subscription.feedback_logging.store([["a1", 1.0], ["a2", 3.4]], fields=["id", "value"])
        """
        validate_type(feedback_data, "feedback_data", list, True)
        validate_type(fields, "fields", list, False)

        self._subscription._engine_client.learning_system.send_feedback(self._subscription.source_uid, feedback_data, fields)

    def show_table(self, limit=10):
        """
        Show records in feedback logging table. By default 10 records will be shown.

        :param limit: maximal number of fetched rows. By default set to 10. (optional)
        :type limit: int

        A way you might use me is:

        >>> subscription.feedback_logging.show_table()
        >>> subscription.feedback_logging.show_table(limit=20)
        >>> subscription.feedback_logging.show_table(limit=None)
        """
        self._validate_if_table_accessible()
        super(FeedbackLogging, self).show_table(limit=limit)

    def print_table_schema(self):
        """
        Show feedback logging table schema.
        """
        self._validate_if_table_accessible()
        super(FeedbackLogging, self).print_table_schema()

    def get_table_content(self, format='pandas', limit=None):
        """
        Get content of feedback logging table in chosen format. By default the format is 'pandas'.

        :param format: format of returned content, may be one of following: ['python', 'pandas'], by default is set 'pandas'
        :type format: {str_type}

        :param limit: maximal number of fetched rows. (optional)
        :type limit: int

        A way you might use me is:

        >>> pandas_table_content = subscription.feedback_logging.get_table_content()
        >>> table_content = subscription.feedback_logging.get_table_content(format='python')
        >>> pandas_table_content = subscription.feedback_logging.get_table_content(format='pandas')
        """
        self._validate_if_table_accessible()
        return super(FeedbackLogging, self).get_table_content(format=format, limit=limit)

    def describe_table(self):
        """
        Describe the content of feedback logging table (pandas style).

        A way you might use me is:

        >>> pandas_table_content = subscription.feedback_logging.describe_table()
        """
        self._validate_if_table_accessible()
        super(FeedbackLogging, self).describe_table()