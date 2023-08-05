# -*- coding: utf-8 -*-

"""upload_to_s3
Downloads a file from S3.
Author: ksco92
"""

import boto3


##########################################
##########################################
##########################################
##########################################

def download_from_s3(file_name, aws_bucket_name, aws_file_path, aws_region_name='us-east-1', aws_access_key_id=None,
                     aws_secret_access_key=None):
    """Downloads a file from the specified bucket and path."""

    if aws_access_key_id and aws_secret_access_key:

        s3 = boto3.resource(service_name='s3',
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=aws_region_name)

    else:
        s3 = boto3.resource(service_name='s3',
                            region_name=aws_region_name)

    if aws_file_path == '':
        full_path = file_name
    else:
        full_path = aws_file_path + '/' + file_name

    s3.Bucket(aws_bucket_name).download_file(full_path, file_name)
