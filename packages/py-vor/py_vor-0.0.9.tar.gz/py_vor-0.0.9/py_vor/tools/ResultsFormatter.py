# -*- coding: utf-8 -*-

"""ResultsFormatter
Object to format results of a query in format of a nested list to a file, format or S3.
Author: ksco92"""

import pandas as pd

from py_vor.tools.upload_to_s3 import upload_to_s3
from py_vor.tools.write_to_csv import write_to_csv


##########################################
##########################################
##########################################
##########################################

class ResultsFormatter:
    """Object to format results of a query in format of a nested list to a file, format or S3."""

    def __init__(self, results, return_as='nested_list', include_headers=True, results_file=None, aws_bucket_name=None,
                 aws_file_path='', aws_region_name='us-east-1', aws_access_key_id=None, aws_secret_access_key=None):
        self.results = results
        self.return_as = return_as
        self.include_headers = include_headers
        self.results_file = results_file
        self.aws_bucket_name = aws_bucket_name
        self.aws_file_path = aws_file_path
        self.aws_region_name = aws_region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    ##########################################
    ##########################################

    def return_results_as(self):

        """Returns the results of a statement in the specified format."""

        if self.return_as == 'nested_list':
            if self.include_headers:
                return self.results
            else:
                return self.results[1:]

        elif self.return_as == 'pd_dataframe':
            results = pd.DataFrame(self.results[1:], columns=self.results[0])
            return results

        elif self.return_as == 'csv_file':
            if self.include_headers:
                write_to_csv(self.results_file, self.results)
            else:
                write_to_csv(self.results_file, self.results[1:])
            return None

        elif self.return_as == 'dict':
            keys = self.results[0]
            values = self.results[1:]
            output = []

            for row in values:
                output.append(dict(zip(keys, row)))

            output = {'data': output}
            return output

        elif self.return_as == 's3_upload':
            if self.include_headers:
                write_to_csv(self.results_file, self.results)
            else:
                write_to_csv(self.results_file, self.results[1:])

            upload_to_s3(self.results_file, self.aws_bucket_name, self.aws_file_path,
                         aws_region_name=self.aws_region_name, aws_access_key_id=self.aws_access_key_id,
                         aws_secret_access_key=self.aws_secret_access_key)

            return None
