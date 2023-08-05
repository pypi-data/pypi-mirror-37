# bi_s3 0.1.9

# Introduction
Data-lake connection object to AWS S3
Easy way to connect and take actions on BI related S3 buckets.
Python 2 & 3 compatible and OS Independent

# API Details

## Installation

To install, run the command below

```
pip install bi_s3
```

and clone the bi_creds repository located here: https://git.pitchbookdata.com/business-intelligence/bi_creds

and run the command below
```
sh /home/$USER/bi_creds/ez_bi_creds_setup.sh
```

If you do not have access to the bi_creds repository, contact Trevor Leider at
trevor.leider@pitchbook.com

## API Methods (only applies to SnowflakeConnection)
* `read_from_s3`: Reads an s3 object and returns it in Pandas dataframe.
* `write_to_s3`: Writes an s3 object.
* `format_for_load` (private): Formats the Pandas DataFrame for database load operation.
* `get_s3_output` (private): Gets the s3 object in a csv format in StringIO format.
* `get_column_names` (private): Gets the column names of s3 object if it exists.
* `get_temp_path` (private): Set up the savepath of the temp file.
* `download_file` (private): Download the s3 object and save it as a temp file.
* `delete_temp_file` (private): Delete the temp file.
* `load_gzip_as_pd` (private): Loads gzip as pandas dataframe.

## Example Usage

### Set up

```python
from bi_s3 import S3BI
s3 = S3BI()
```
### read_from_s3 example

```python
# if_exists is a key argument. If not specified, it defaults to "append"
s3.read_from_s3(filepath="s3://pitchbook-snowflake/path/to/file", nrows=50, usecols=["col", "names"])
```

### write_to_s3 example

```python
s3.write_to_s3(df=pandas_dataframe, savepath="s3://pitchbook-snowflake/path/to/file")
```
