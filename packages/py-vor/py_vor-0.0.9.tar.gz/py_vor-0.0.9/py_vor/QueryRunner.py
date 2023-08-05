# -*- coding: utf-8 -*-

"""QueryRunner
Object to run queries from SQL files and return them in a specified format.
Author: ksco92
"""

from py_vor.tools.CursorFactory import CursorFactory
from py_vor.tools.ResultsFormatter import ResultsFormatter


##########################################
##########################################
##########################################
##########################################

class QueryRunner:
    """Object to run queries from SQL files and return them in a specified format."""

    def __init__(self, engine, host, port, username, password, schema, sql_file, autocommit=False, returns_rows=False,
                 text_to_replace=None, replace_text_with=None, include_headers=True, return_as='nested_list',
                 results_file=None, aws_access_key_id=None, aws_secret_access_key=None, aws_region_name='us-east-1',
                 aws_bucket_name=None, aws_file_path=''):
        self.engine = engine
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.schema = schema
        self.autocommit = autocommit
        self.returns_rows = returns_rows
        self.sql_file = sql_file
        self.text_to_replace = text_to_replace
        self.replace_text_with = replace_text_with
        self.include_headers = include_headers
        self.return_as = return_as
        self.results_file = results_file
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region_name = aws_region_name
        self.aws_bucket_name = aws_bucket_name
        self.aws_file_path = aws_file_path
        self.statements = self.get_statements()

    ##########################################
    ##########################################

    def execute_all(self):

        """Executes the results of all the queries in the specified file and returns the results of the last one in the
        specified format."""

        cur = self.get_cursor()
        results = []

        for statement in self.statements:
            results = self.execute_statement(cur, statement)

        if self.returns_rows:
            return self.return_results_as(results)

        else:
            return results

    ##########################################
    ##########################################

    def get_cursor(self):

        """Gets a cursor based on the engine name."""

        return CursorFactory(self.engine, self.host, self.port, self.username, self.password, self.schema,
                             autocommit=self.autocommit).create_cursor()

    ##########################################
    ##########################################

    def execute_statement(self, cur, statement):

        """Executes a SQL statement using the provided cursor."""

        query_results = []
        column_names = []

        cur.execute(statement)

        if self.returns_rows:

            for col in cur.description:
                if self.engine in ('mysql', 'sqlserver'):
                    column_names.append(col[0])
                elif self.engine in ('redshift', 'postgresql'):
                    column_names.append(col[0].decode("utf-8"))

            query_results.append(column_names)

            for row in cur:
                row = [str(n) for n in row]
                query_results.append(list(row))

        else:
            return None

        return query_results

    ##########################################
    ##########################################

    def get_statements(self):

        """Reads the queries in the provided file and replaces the desired text."""

        with open(self.sql_file) as f:
            query = f.read()
            f.close()

        if self.text_to_replace and self.replace_text_with:
            for ttr, rtw in zip(self.text_to_replace, self.replace_text_with):
                query = query.replace(ttr, rtw)

        queries = query.split(';')
        queries = list(filter(None, queries))

        return queries

    ##########################################
    ##########################################

    def return_results_as(self, results):

        """Returns the results of a statement in the specified format."""

        return ResultsFormatter(results, return_as=self.return_as, include_headers=self.include_headers,
                                results_file=self.results_file, aws_bucket_name=self.aws_bucket_name,
                                aws_file_path=self.aws_file_path, aws_region_name=self.aws_region_name,
                                aws_access_key_id=self.aws_access_key_id,
                                aws_secret_access_key=self.aws_secret_access_key).return_results_as()
