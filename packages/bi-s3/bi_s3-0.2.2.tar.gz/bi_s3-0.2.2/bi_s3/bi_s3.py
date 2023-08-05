import boto3
import botocore
import pandas as pd
import gzip
import json
import os
from io import BytesIO
import sys
if sys.version_info >= (3,0):
    from io import StringIO
else:
    from StringIO import StringIO
from botocore.exceptions import ClientError
from biz_intel_creds import CredsList
dev_s3_creds = CredsList().dev_s3
bi_s3_creds = CredsList().bi_s3

class S3BI(object):
    def __init__(self, bucket_name="pitchbook-snowflake"):
        """Data-lake connection object to AWS S3

        Args:
            NA
        Returns:
            NA
        Raises:
            NA
        """
        self.bucket_name = bucket_name.lower()
        if self.bucket_name == "pitchbook-snowflake":
            self.client = boto3.client('s3',
                aws_access_key_id=bi_s3_creds['aws_access_key_id'],
                aws_secret_access_key=bi_s3_creds['key']
            )
        elif self.bucket_name == "pb-unified-usage-data-source":
            self.client = boto3.client('s3',
                aws_access_key_id=dev_s3_creds['aws_access_key_id'],
                aws_secret_access_key=dev_s3_creds['key']
            )
        else:
            raise ValueError(
                "bucket_name: {} not supported yet".format(self.bucket_name))

    def read_from_s3(self, filepath, **kwargs):
        """Reads an s3 object and returns it in Pandas dataframe

        Args:
            filepath (str): the filepath of s3 object
        Returns:
            df (pandas dataframe): pandas dataframe of the s3 object
        Raises:
            NA
        """
        if "nrows" in kwargs:
            nrows = kwargs["nrows"]
        else:
            nrows = None

        if "usecols" in kwargs:
            usecols = kwargs["usecols"]
        else:
            usecols = None

        if "return_as_list" in kwargs:
            return_as_list = kwargs["return_as_list"]
        else:
            return_as_list = False

        s3_prefix = "s3://{bn}/".format(bn=self.bucket_name)
        if s3_prefix in filepath:
            filepath = filepath.replace(s3_prefix, "")

        if ".gz" in filepath.lower():
            self._download_file(filepath, filetype="gz")
            if return_as_list == True:
                list_of_dicts = self._load_gzip_as_dict_list()
                self._delete_temp_file()
                return list_of_dicts
            else:
                df = self._load_gzip_as_pd()
            self._delete_temp_file()
        else:
            self._download_file(filepath, filetype="csv")
            if ".csv" not in filepath.lower():
                df = pd.read_csv(self.temp_path, header=None,
                    error_bad_lines=False, low_memory=True,
                    nrows=nrows, usecols=usecols)
            else:
                df = pd.read_csv(self.temp_path, error_bad_lines=False,
                    low_memory=True, nrows=nrows, usecols=usecols)
            self._delete_temp_file()
        col_names = self._get_column_names(filepath)

        if "staging_file" in filepath.lower():
            pass
        elif isinstance(col_names, list) and "column_names.csv" not in filepath:
            df.columns = col_names
        else:
            pass
        df = self._format_for_load(df)
        return df

    def write_to_s3(self, df, savepath):
        """Writes an s3 object

        Args:
            df (pandas dataframe): the dataframe you want to write to s3

            savepath (str): the filepath to s3 object
        Returns:
            NA
        Raises:
            NA
        """
        if ".gz" in savepath.lower():
            filetype = "gz"
        else:
            filetype = "csv"

        s3_prefix = "s3://{bn}/".format(bn=self.bucket_name)
        if s3_prefix in savepath:
            savepath = savepath.replace(s3_prefix, "")

        df = self._format_for_load(df)
        if sys.version_info >= (3,0):
            buffer = StringIO()
        else:
            buffer = BytesIO()
        if filetype == "csv":
            df.to_csv(buffer, index=False)
        elif filetype == "gz":
            if str(type(df)) == "<class 'pandas.core.frame.DataFrame'>":
                json_str = df.to_json(compression="gzip", orient="records")
                json_str = json_str.replace("[", "").replace("]", "").\
                    replace("},", "}\n") + "\n"
                with gzip.GzipFile(fileobj=buffer, mode="w") as f:
                  f.write(json_str)
            else:
                formatted_json_list = [json.dumps(x) for x in df]
                formatted_json_list = map(str, formatted_json_list)
                json_str = "\n".join(formatted_json_list)
                with gzip.GzipFile(fileobj=buffer, mode="w") as f:
                    f.write(json_str)
        response = self.client.put_object(
        	Body=buffer.getvalue(),
        	ContentType='application/vnd.ms-excel',
        	Bucket=self.bucket_name,
        	Key=savepath,
        )
        buffer.close()

    def _format_for_load(self, df):
        """Formats the dataframe for load operation to a SQL db

        Args:
            df (pandas dataframe): the dataframe you want to upload to db
        Returns:
            NA
        Raises:
            NA
        """
        try:
            datetime_cols = [x for x in df.columns if "_date" in x.lower()]
        except AttributeError as e:
            new_header = df.iloc[0]
            df = df[1:]
            df.columns = new_header
            datetime_cols = [x for x in df.columns if "_date" in x.lower()]
        except:
            raise ValueError("check your s3 object input")
        for col in datetime_cols:
            df[col] = pd.to_datetime(df[col], errors = 'coerce')
        # if all values for the given column is na, then set it to string
        for col in df.columns:
            if df[col].isnull().all():
                df[col] = df[col].astype(str)
        df = df.replace({'NaT': pd.np.nan, 'None': pd.np.nan,
            None: pd.np.nan, pd.NaT: pd.np.nan})
        return df

    def _get_s3_output(self, filepath):
        """Gets the s3 object in a csv format in StringIO format

        Args:
            filepath (str): the filepath of column names s3 object
        Returns:
            output (str): csv s3 object in string
        Raises:
            NA
        """
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=self.bucket_name, Key=filepath)
        body = obj['Body']
        csv_string = body.read().decode('utf-8')
        output = StringIO(csv_string)
        output.seek(0)
        return output

    def _get_column_names(self, filepath):
        """Gets the column names of s3 object if it exists

        Args:
            filepath (str): the filepath of column names s3 object
        Returns:
            result: list of column names or None
        Raises:
            ClientError: if the s3 object does not exist
        """
        filepath = filepath.rsplit('/', 1)[0]
        filepath = filepath + "/column_names.csv"
        try:
            output = self._get_s3_output(filepath)
            df = pd.read_csv(output, low_memory=True)
            output.close()
            result = list(df.column_name.unique())
        except ClientError as ex:
            result = None
        return result

    def _get_temp_path(self, file_type="csv"):
        """Set up the savepath of the temp file

        Args:
            NA
        Returns:
            NA
        Raises:
            NA
        """
        import getpass
        import platform
        import random
        random_num = random.randint(1,101)
        username = getpass.getuser()
        op_sys = platform.system()
        if op_sys == "Windows":
            temp_path = "C:/Users/{username}/tempfile_{ri}.{filetype}".format(
                username=username, filetype=file_type, ri=random_num
            )
        elif op_sys == "Linux":
            temp_path = "/home/{username}/tempfile_{ri}.{filetype}".format(
                username=username, filetype=file_type, ri=random_num
            )
        else:
            raise OSError(
              "operating system: {op_sys} not supported".format(op_sys=op_sys))
        return temp_path

    def _download_file(self, filepath, filetype):
        """Download the s3 object and save it as a temp file

        Args:
            NA
        Returns:
            NA
        Raises:
            NA
        """
        self.temp_path = self._get_temp_path(filetype)
        try:
            os.remove(self.temp_path)
        except OSError:
            pass
        self.client.download_file(self.bucket_name, filepath, self.temp_path)

    def _delete_temp_file(self):
        """Delete the temp file

        Args:
            NA
        Returns:
            NA
        Raises:
            NA
        """
        import os
        os.remove(self.temp_path)

    def _load_gzip_as_pd(self):
        """Loads gzip as pandas dataframe

        Args:
            NA
        Returns:
            df (pandas dataframe): pandas dataframe of the s3 object
        Raises:
            NA
        """
        file_name = gzip.open(self.temp_path)
        file_content = file_name.read()
        formatted_file = file_content.split("\n")
        del formatted_file[-1] #Deleting the empty value on the end
        list_of_data = []
        for i in formatted_file:
            try:
                list_of_data.append(json.loads(i))
            except:
                ValueError("Unable to parse gzip JSON.")
        df = pd.DataFrame(list_of_data)
        file_name.close()
        return df

    def _load_gzip_as_dict_list(self):
        """Loads gzip as a list of dictionaries

        Args:
            NA
        Returns:
            list_of_dicts (list of dictionaries): list of dictionaries of the s3 JSON object
        Raises:
            NA
        """
        file_name = gzip.open(self.temp_path)
        file_content = file_name.read()
        formatted_file = file_content.split("\n")
        del formatted_file[-1]
        list_of_dicts = []
        for i in formatted_file:
            try:
                list_of_dicts.append(json.loads(i))
            except:
                ValueError("Unable to parse gzip JSON.")
        file_name.close()
        return list_of_dicts
