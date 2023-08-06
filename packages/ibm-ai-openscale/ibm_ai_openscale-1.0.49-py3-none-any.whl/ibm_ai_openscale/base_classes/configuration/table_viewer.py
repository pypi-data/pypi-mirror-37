import logging
from ibm_ai_openscale.base_classes import Table
from ibm_ai_openscale.utils import *


_DEFAULT_LIST_LENGTH = 50


class TableViewer:
    def __init__(self, ai_client, subscription, configuration, table_name=None, schema=None, conditions={}):
        self._logger = logging.getLogger(__name__)
        self._ai_client = ai_client
        self._subscription = subscription
        self._configuration = configuration
        self._table_name = table_name
        self._schema = schema
        self._conditions = conditions

    def _get_connection_data(self):
        details = self._ai_client.data_mart.get_details()
        store = details['database_configuration']
        creds = store['credentials']
        uri = creds['uri']

        res = re.search('^[0-9a-zA-Z]+://([0-9a-zA-Z]+):([0-9a-zA-Z]+)@([^:]+):([0-9]+)/([0-9a-zA-Z]+)$', uri)

        if res is None:
            raise ClientError('Unexpected format of db uri: {}'.format(uri))

        username = res.group(1)
        password = res.group(2)
        host = res.group(3)
        port = res.group(4)
        database = res.group(5)

        if not configuration_details['enabled']:
            raise ClientError('Required monitoring/logging is not enabled.')

        if self._table_name is not None:
            table_name = self._table_name
        elif 'parameters' in configuration_details and 'table_name' in configuration_details['parameters']:
            if '.' in configuration_details['parameters']['table_name']:
                table_name = configuration_details['parameters']['table_name'].split('.')[1]
            else:
                table_name = configuration_details['parameters']['table_name']
        else:
            raise ClientError('Either parameters of monitoring/logging are missing or table_name is not defined.')

        if self._schema is not None:
            schema = self._schema
        else:
            schema = store['location']['schema']

        connection_data = {
            "type": store['database_type'],
            "database": database,
            "user": username,
            "password": password,
            "host": host,
            "port": port,
            "tablename": table_name,
            "schema": schema
        }

        return connection_data

    @staticmethod
    def _db_connect(connection_data):
        import psycopg2

        conn = psycopg2.connect(
            database=connection_data['database'],
            user=connection_data['user'],
            password=connection_data['password'],
            host=connection_data['host'],
            port=connection_data['port'],
            options='-c search_path=\"{}\"'.format(connection_data['schema']) # TODO secure it
        )

        return conn

    def show_table(self, limit=10):
        """
        Show records in payload logging table. By default 10 records will be shown.

        :param limit: maximal number of fetched rows. By default set to 10. (optional)
        :type limit: int

        A way you might use me is:

        >>> client.payload_logging.show_table()
        >>> client.payload_logging.show_table(limit=20)
        >>> client.payload_logging.show_table(limit=None)
        """
        validate_type(limit, u'limit', int, False)

        result = self.get_table_content(format='python', limit=limit)

        rows = result['values']
        col_names = result['fields']

        cond_str = ''
        if len(self._conditions) > 0:
            cond_str = ' ({})'.format(', '.join([key + '=' + value for key, value in self._conditions.items()]))

        connection_data = self._get_connection_data()

        Table(col_names, rows).list(limit=limit, default_limit=_DEFAULT_LIST_LENGTH, title=connection_data['tablename'] + cond_str)

    def print_table_schema(self):
        """
        Show table schema.
        """
        connection_data = self._get_connection_data()
        conn = self._db_connect(connection_data)

        try:
            from psycopg2.sql import Identifier, SQL

            cur = conn.cursor()

            cur.execute("SELECT oid, typname from pg_type")
            types = {key: value for (key, value) in cur}

            cur.execute(SQL("SELECT * from {} fetch first 1 rows only").format(Identifier(connection_data['tablename'])))
            description = [(
                desc[0],
                types[desc[1]],
                desc[3] if desc[3] != -1 else '-',
                desc[4] if desc[4] is not None else '-',
                desc[5] if desc[5] is not None else '-',
                'Y' if desc[6] is not None else 'N'
            ) for desc in cur.description]

            Table(['name', 'type', 'size', 'precision', 'scale', 'nullable'], description).list(title='Schema of ' + connection_data['tablename'])
        except Exception as e:
            self._logger.debug('Error during getting required info from db: {}'.format(e))
            raise ClientError('Error during getting required info from db.')
        finally:
            conn.close()

    def get_table_content(self, format='pandas', limit=None):
        """
        Get content of table in chosen format. By default the format is 'pandas'.

        :param format: format of returned content, may be one of following: ['python', 'pandas'], by default is set 'pandas'
        :type format: {str_type}

        :param limit: maximal number of fetched rows. (optional)
        :type limit: int

        A way you might use me is:

        >>> pandas_table_content = client.get_table_content()
        >>> table_content = client.get_table_content(format='python')
        >>> pandas_table_content = client.get_table_content(format='pandas')
        """
        validate_type(format, u'format', str, True)

        if format not in ['python', 'pandas']:
            raise ClientError('Unsupported format chosen: {}'.format(format))

        connection_data = self._get_connection_data()
        conn = self._db_connect(connection_data)

        try:
            from psycopg2.sql import Identifier, SQL

            cur = conn.cursor()
            sql_query = "SELECT * from {}"
            identifiers = [Identifier(connection_data['tablename'])]
            params = []

            if len(list(self._conditions.keys())) > 0:
                sql_query += ' where ' + ' and '.join(['{}=%s'] * len(list(self._conditions.keys())))

                for key, value in self._conditions.items():
                    identifiers.append(Identifier(key))
                    params.append(value)

            if limit is not None:
                sql_query += ' fetch first %s rows only'
                params.append(limit + 1)

            cur.execute(SQL(sql_query).format(*identifiers), params)

            col_names = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
        except Exception as e:
            self._logger.debug('Error during getting required info from db: {}'.format(e))
            raise ClientError('Error during getting required info from db.')
        finally:
            conn.close()

        if format == 'python':
            return {'fields': col_names, 'values': rows}
        elif format == 'pandas':
            import pandas as pd
            return pd.DataFrame.from_records(rows, columns=col_names)
        else:
            raise ClientError('Unsupported format chosen: {}'.format(format))

    def describe_table(self):
        """
        Describe the content of table (pandas style). It will remove columns with unhashable values.

        :return: description/summary
        :rtype: DataFrame

        A way you might use me is:

        >>> description = client.describe_table()
        """
        df = self.get_table_content(format='pandas')

        columns_to_remove = []
        for column_name in list(df):
            try:
                df[column_name].describe()
            except:
                columns_to_remove.append(column_name)

        df = df.drop(columns=columns_to_remove)
        description = df.describe()
        print(description)
        return description
