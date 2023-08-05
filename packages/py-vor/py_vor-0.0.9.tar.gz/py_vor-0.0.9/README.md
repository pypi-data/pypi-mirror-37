- [py_vor](#py-vor)
  * [Main objects](#main-objects)
    + [QueryRunner](#queryrunner)
      - [args](#args)
      - [kwargs](#kwargs)
      - [Examples](#examples)
        * [Nested list without headers](#nested-list-without-headers)
        * [Nested list with headers](#nested-list-with-headers)
        * [Dict](#dict)
        * [Pandas data frame](#pandas-data-frame)
  * [Tools](#tools)
    + [get_secret](#get-secret)
      - [args](#args-1)
      - [kwargs](#kwargs-1)
      - [Examples](#examples-1)
    + [download_from_s3](#download-from-s3)
      - [args](#args-2)
      - [kwargs](#kwargs-2)
      - [Examples](#examples-2)
        * [Straight from bucket](#straight-from-bucket)
        * [With additional path](#with-additional-path)
    + [upload_to_s3](#upload-to-s3)
      - [args](#args-3)
      - [kwargs](#kwargs-3)
      - [Examples](#examples-3)
        * [Straight to bucket](#straight-to-bucket)
        * [With additional path](#with-additional-path-1)
  * [Uploaded to PyPI by using](#uploaded-to-pypi-by-using)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

# py_vor

This library is intended to ease the use basic operations for data retrieval or storage for BI. This library is still in development.

## Main objects

### QueryRunner

Object to run queries from SQL files and return them in a specified format.

#### args

* `engine`: Name of the DB engine to run queries on. Supported engines are:
    * `mysql`
    * `sqlserver`
    * `redshift`
    * `postgresql`
* `host`: Host name of the DB to run queries on.
* `port`: Port number of the DB to run queries on.
* `username`: Username to connect to the DB with.
* `password`: Password for the user to connect to the DB with.
* `schema`: Default schema to run queries on.
* `sql_file`: Location of the file that has the queries to run.

#### kwargs

* `autocommit=False`: Whether the cursor will have autocommit on or off. Can only be `True` or `False`.
* `returns_rows=False`: Whether the query returns rows or not. Use `False` for basically everything other than `SELECT` statements.
* `text_to_replace=None`: List of strings to replace the strings in the `replace_text_with` kwarg. Must be the same length of `replace_text_with`.
* `replace_text_with=None`: List of strings to replace the strings in the `text_to_replace` kwarg. Must be the same length of `text_to_replace`.
* `include_headers=True`: If `return_as` is `nested_list`, `csv_file` or `s3_upload`, this will determine if the results include the column names or not.
* `return_as='nested_list'`: Determines the format for the results to be returned. Can be:
    * `nested_list`: List of lists, where each inner list is a row of the results.
    * `csv_file`: CSV file where each row is a row of the results.
    * `s3_upload`: Same as CSV but uploads the results file to S3 and the deletes the local file.
    * `dict`: Each row is a dictionary in a list inside of `{'data': [output]}`.
    * `pd_dataframe`: Pandas standard data frame.
* `results_file=None`: Name and location of the file to put the results on. Only works when `return_as` is `csv_file` or `s3_upload`.
* `aws_access_key_id=None`: AWS Access Key ID. Can remain as `None` if AWS CLI has the keys configured or IAM role is set up in host.
* `aws_secret_access_key=None`: AWS Secret Access Key. Can remain as `None` if AWS CLI has the keys configured or IAM role is set up in host.
* `aws_region_name='us-east-1'`: Default AWS region name.
* `aws_bucket_name=None`: Bucket to put the results on. Only works if `resturn_as` is `s3_upload`.
* `aws_file_path=''`: S3 path after bucket to put the file on. Does not include the actual file name, for that use the `results_file` kwarg.

#### Examples

##### Nested list without headers

```python 
>>> from py_vor.tools.get_secret import get_secret
>>> from py_vor.QueryRunner import QueryRunner
>>> secret = get_secret('aws_secret_name')
>>> runner = QueryRunner(secret['engine'], secret['host'], secret['port'], secret['username'], secret['password'],secret['dbname'], 'select_user.sql', returns_rows=True, include_headers=False)
>>> results = runner.execute_all()
>>> results
[['10001', '1953-09-02', 'Georgi', 'Facello', 'M', '1986-06-26']]
>>> 
```

##### Nested list with headers

```python 
>>> from py_vor.tools.get_secret import get_secret
>>> from py_vor.QueryRunner import QueryRunner
>>> secret = get_secret('aws_secret_name')
>>> runner = QueryRunner(secret['engine'], secret['host'], secret['port'], secret['username'], secret['password'],secret['dbname'], 'select_user.sql', returns_rows=True)
>>> results = runner.execute_all()
>>> results
[['emp_no', 'birth_date', 'first_name', 'last_name', 'gender', 'hire_date'], ['10001', '1953-09-02', 'Georgi', 'Facello', 'M', '1986-06-26']]
>>>
```

##### Dict

```python 
>>> from py_vor.tools.get_secret import get_secret
>>> from py_vor.QueryRunner import QueryRunner
>>> secret = get_secret('aws_secret_name')
>>> runner = QueryRunner(secret['engine'], secret['host'], secret['port'], secret['username'], secret['password'],secret['dbname'], 'select_user.sql', returns_rows=True, return_as='dict')
>>> results = runner.execute_all()
>>> results
{'data': [{'emp_no': '10001', 'birth_date': '1953-09-02', 'first_name': 'Georgi', 'last_name': 'Facello', 'gender': 'M', 'hire_date': '1986-06-26'}]}
>>> 
```

##### Pandas data frame

```python 
>>> from py_vor.tools.get_secret import get_secret
>>> from py_vor.QueryRunner import QueryRunner
>>> secret = get_secret('aws_secret_name')
>>> runner = QueryRunner(secret['engine'], secret['host'], secret['port'], secret['username'], secret['password'],secret['dbname'], 'select_user.sql', returns_rows=True, return_as='pd_dataframe')
>>> results = runner.execute_all()
>>> results
  emp_no  birth_date first_name last_name gender   hire_date
0  10001  1953-09-02     Georgi   Facello      M  1986-06-26
>>> 
```

## Tools

### get_secret

Gets secret from AWS Secrets Manager.

#### args

* `secret_name`: Name of the secret in AWS Secrets Manager.

#### kwargs

* `aws_access_key_id=None`: AWS Access Key ID. Can remain as `None` if AWS CLI has the keys configured or IAM role is set up in host.
* `aws_secret_access_key=None`: AWS Secret Access Key. Can remain as `None` if AWS CLI has the keys configured or IAM role is set up in host.
* `aws_region_name='us-east-1'`: Default AWS region name.

#### Examples

```python 
>>> from py_vor.tools.get_secret import get_secret
>>> secret = get_secret('aws_secret_name')
>>> secret
{'username': 'dbusername', 'password': 'pswd', 'engine': 'mysql', 'host': 'localhost', 'port': 3306, 'dbname': 'default_schema', 'dbInstanceIdentifier': 'instanceID'}
>>>
```

### download_from_s3

Download a file from S3.

#### args

* `file_name`: Name of the file to download from S3.
* `aws_bucket_name`: Name of the the bucket the file is located on. 
* `aws_file_path`: Path where the file is located

#### kwargs

* `aws_access_key_id=None`: AWS Access Key ID. Can remain as `None` if AWS CLI has the keys configured or IAM role is set up in host.
* `aws_secret_access_key=None`: AWS Secret Access Key. Can remain as `None` if AWS CLI has the keys configured or IAM role is set up in host.
* `aws_region_name='us-east-1'`: Default AWS region name.

#### Examples

##### Straight from bucket

```python 
>>> from py_vor.tools.download_from_s3 import download_from_s3
>>> bucket_name = 'bucket-name'
>>> download_from_s3('my_file.txt', bucket_name, '')
>>> 
```

##### With additional path

```python 
>>> from py_vor.tools.download_from_s3 import download_from_s3
>>> bucket_name = 'bucket-name'
>>> download_from_s3('my_file.txt', bucket_name, 'subfolder1/subfolder2')
>>> 
```

### upload_to_s3

Upload a file to S3.

#### args

* `file_name`: Name of the file to download from S3.
* `aws_bucket_name`: Name of the the bucket the file is located on. 
* `aws_file_path`: Path where the file is located

#### kwargs

* `aws_access_key_id=None`: AWS Access Key ID. Can remain as `None` if AWS CLI has the keys configured or IAM role is set up in host.
* `aws_secret_access_key=None`: AWS Secret Access Key. Can remain as `None` if AWS CLI has the keys configured or IAM role is set up in host.
* `aws_region_name='us-east-1'`: Default AWS region name.

#### Examples

##### Straight to bucket

```python 
>>> from py_vor.tools.upload_to_s3 import upload_to_s3
>>> bucket_name = 'bucket-name'
>>> upload_to_s3('my_file.txt', bucket_name, '')
>>>
```

##### With additional path

```python 
>>> from py_vor.tools.upload_to_s3 import upload_to_s3
>>> bucket_name = 'bucket-name'
>>> upload_to_s3('my_file.txt', bucket_name, 'subfolder1/subfolder2')
>>>
```

## Uploaded to PyPI by using

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```
