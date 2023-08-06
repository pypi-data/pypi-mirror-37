import os
from google.cloud import spanner


class SpannerClient:
    class __SpannerClient:
        def __init__(self):
            self.client = spanner.Client(os.environ.get("PROJECT"))
            self.spanner_instance = self.client.instance(os.environ.get("PROJECT"))

    instance = None

    def __init__(self):
        if not SpannerClient.instance:
            SpannerClient.instance = SpannerClient.__SpannerClient()

    def get_database(self, database_id):
        """
        Get a spanner Database object referencing the id provided
        :param database_id: str, id of spanner database
        :return: Database
        """
        return self.spanner_instance.database(database_id)

    @staticmethod
    def read_data(database, table, keys, columns, all_=False):
        """
        query a table by primary(ies) key(s) and retrieve the given columns
        :param database: Database, reference of the database
        :param table: str, table to search
        :param keys: tuple<str>, primary keys
        :param columns: tuple<str>, columns to retrieve
        :param all_: boolean, true
        :return: StreamedResultSet, Iterator with list as rows, each list has the values of the columns
        """
        with database.snapshot() as snapshot:
            key_set = spanner.KeySet(keys=keys) if not all_ else spanner.KeySet(all_=True)
            results = snapshot.read(
                table=table,
                columns=columns,
                keyset=key_set, )
            return results

    @staticmethod
    def query_data(database, sql_statement):
        """
        query a table by sql statement and retrieve the given columns
        :param database: Database, reference of the database
        :param sql_statement: str, sql statement
        :return: StreamedResultSet, Iterator with list as rows, each list has the values of the columns
        """
        with database.snapshot() as snapshot:
            results = snapshot.execute_sql(sql_statement)
            return results

    @staticmethod
    def insert_data(database, table, columns, value=None, values=None):
        """
        Insert row(s) into the given column on the given database
        :param database: Database, reference of the database
        :param table: str, table to insert
        :param columns: tuple<str>, columns to insert
        :param value: tuple, values matching the columns to insert
        :param values: list<tuple>, list of value object
        """
        if value:
            values = [value]
        with database.batch() as batch:
            batch.insert(table=table,
                         columns=columns,
                         values=values)

    @staticmethod
    def update_data(database, table, columns, value=None, values=None):
        """
        Update row(s) into the given column on the given database
        :param database: Database, reference of the database
        :param table: str, table to update
        :param columns: tuple<str>, columns to update
        :param value: tuple, values matching the columns to update
        :param values: list<tuple>, list of value object
        """
        if value:
            values = [value]
        with database.batch() as batch:
            batch.update(table=table,
                         columns=columns,
                         values=values)

    @staticmethod
    def delete_data(database, table, keys):
        """
        Delete row(s) with the given keys
        :param database: Database, reference of the database
        :param table:
        :param keys:
        """
        with database.batch() as batch:
            key_set = spanner.KeySet(keys=keys)
            batch.delete(table, key_set)

    def __getattr__(self, name):
        return getattr(self.instance, name)
