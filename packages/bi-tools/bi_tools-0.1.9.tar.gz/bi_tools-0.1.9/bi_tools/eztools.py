from __future__ import print_function
import pandas as pd
import os
import getpass
import argparse
import subprocess
import logging
import boto3
import botocore
from datetime import datetime
from datetime import timedelta
from bi_tools.bi_exceptions import BackfillException
from bi_tools.bi_exceptions import SnowflakeException
from botocore.exceptions import ClientError
from io import BytesIO
import sys
if sys.version_info >= (3,0):
    from io import StringIO
else:
    from StringIO import StringIO
from bi_s3 import S3BI
global username
username = getpass.getuser()

def wide_to_long(df, stubnames, i, j):
    """ Just a wrapper of pandas wide_to_long function
    """
    import pandas as pd
    df= pd.wide_to_long(df, stubnames, i , j)
    return df

def long_to_wide(df, stub, i, j, drop_others=False):
    """ Long to wide panel format. Less flexible but more user friendly than
    pivot tables to get a stata-like reshape.

    This function expects to find a stub column, with values in its rows
    uniquely identified by values in columns i and j. The values in j
    will be applied as suffixes to the stub column to generate a group of
    columns with format Asuffix1, Asuffix2,...AsuffixN.

    Note - will treat all extra columns not included in reshape as additional
    ID columns. The only reason they need to be passed is to ensure that the
    data SHOULD be reshaped, since given enough columns pretty much anything
    can uniquely identify a row.

    Arguments:
    df : DataFrame
         The long-format DataFrame
    stub : str
          The stub name. Contains values in long format. The wide format
          columns will start with this stub name.
    i : str or list
        Columns to use as id variables. Together with j, should uniquely
        identify an observation in a row in stub
    j : str
        Extant column with observations to use as suffix for the stub name.
    drop_others : bool, default=False
                If true, will drop any columns not specified in either i or j.
                Otherwise all columns will be included as additional
                identifier columns.
    """
    if type(i) is str:
        i = [i]
    if isinstance(df.index, pd.core.index.MultiIndex):
        df = df.reset_index()
    # Error Checking
    if df[i + [j]].duplicated().any():
        raise ValueError("i and j don't uniquely identify each row")

    # Perform reshape
    if drop_others:
        df = df[i + [j]]
    else:
        i = [x for x in list(df) if x not in [stub, j]]

	#i = [x for x in i if x not in ["code_system", "extract_type_id"]]

    df = df.set_index(i + [j]).unstack()
    # Ensure all stubs and suffixes are strings and join them to make col names
    cols = pd.Index(df.columns)
    # for each s in each col in cols, e.g. cols = [(s, s1), (s, s2)]
    cols = map(lambda col: map(lambda s: str(s), col), cols)
    cols = [''.join(c) for c in cols]
    # Set columns to the stub+suffix name and remove MultiIndex
    df.columns = cols
    df = df.reset_index()
    return df

def create_hash_key(df, col_list):
    import hashlib
    df["gamma_id"] = ""
    for col in col_list:
        df["gamma_id"] += df[col].astype(str)
    df['gamma_id'] = [hashlib.md5(val).hexdigest() for val in df['gamma_id']]
    return df

def remove_garbage(garbage):
    import gc
    if garbage in globals():
        del globals()[garbage]
    else:
        pass
    gc.collect()

def redshift_to_snowflake(schema, table):
    from bi_db import RedshiftConnection
    from bi_db import SnowflakeConnection
    from datetime import datetime
    rc = RedshiftConnection()
    sc = SnowflakeConnection()
    schema = schema.upper()
    table = table.upper()
    filepath = "s3://pitchbook-snowflake/schema={schema}/table={table}/"\
        "{date}/{schema}_{table}000".format(
            schema=schema,
            table=table,
            date=datetime.strftime(datetime.today(), "%Y-%m-%d")
        )
    rc.unload(database="dev", schema=schema, table=table)
    sc.load(db_name="BUSINESS_INTELLIGENCE",
            schema_name=schema,
            table_name=table,
            filepath=filepath,
            format="csv")
    return "done"

def flex_write(df, save_path, file_type="csv", **kwargs):
    if "s3" in kwargs:
        save_in_s3 = kwargs["s3"]
        if "bucket_name" in kwargs:
            bucket_name = kwargs["bucket_name"]
        else:
            bucket_name = "pitchbook-snowflake"
    else:
        save_in_s3 = False

    if save_in_s3 == True:
        s3bi = S3BI(bucket_name=bucket_name)
        s3bi.write_to_s3(df, save_path)
    else:
        if file_type.lower() == "h5":
            file_type = "hdf"
        flex_write = getattr(df, 'to_{}'.format(file_type))

        if file_type.lower() == "csv":
            flex_write(save_path, index=False)
        elif file_type.lower() == "hdf":
            flex_write(save_path, "w")

        print("{filetype} saved here: {savepath}".format(filetype=file_type,
                                                        savepath=save_path))

def flex_read(load_path, **kwargs):
    if "s3" in kwargs:
        load_from_s3 = kwargs["s3"]
        if "bucket_name" in kwargs:
            bucket_name = kwargs["bucket_name"]
        else:
            bucket_name = "pitchbook-snowflake"
    else:
        load_from_s3 = False

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

    if load_from_s3:
        s3bi = S3BI(bucket_name=bucket_name)
        if return_as_list:
            df = s3bi.read_from_s3(load_path, return_as_list=return_as_list)
        else:
            df = s3bi.read_from_s3(load_path, nrows=nrows, usecols=usecols)
    else:
        file_type = load_path.split(".")[-1]
        flex_load = getattr(pd, 'read_{}'.format(file_type))
        df = flex_load(load_path)
        print("Loaded {filetype} from {loadpath}".format(filetype=file_type,
                                                            loadpath=load_path))
    return df

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed

def backfill(filepath, start_date, end_date):
    import bi_db
    shell_path = bi_db.__file__.replace("bi_db", "bi_tools")\
                    .replace(bi_db.__file__.split("/")[-1], "backfill.sh")
    try:
        subprocess.Popen(['chmod', '777', shell_path])
        subprocess.Popen(['sh', shell_path, filepath, start_date, end_date])
    except OSError:
        raise BackfillException("You do not have the shell script in" \
                                "{shellpath}".format(shellpath=shell_path))
    print("backfill job submitted")

def col_type_compare_and_match(df, db_df):
    if len(db_df) > 0:
        df_types = dict(df.dtypes)
        db_types = dict(db_df.dtypes)

        def convert_str_to_unicode(dict_to_convert):
            for key, value in dict_to_convert.items():
                # for now, assume any 'object' variable is unicode
                if value == object:
                    dict_to_convert[key] = type("str")
            return dict_to_convert

        df_types = convert_str_to_unicode(df_types)
        db_types = convert_str_to_unicode(db_types)

        cols_to_convert = []
        sharedKeys = set(df_types.keys()).intersection(db_types.keys())
        for key in sharedKeys:
            if df_types[key] != db_types[key]:
                cols_to_convert.append(key)

        for col in cols_to_convert:
            df[col] = df[col].astype(db_types[col])
    else:
        pass

    return df

def format_for_load(df):
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

    # per sarah's request
    for col in df.columns:
        if "_id" in col.lower():
            df[col] = df[col].fillna(0).astype(int)
            df[col] = df[col].astype(int)
        elif "_min" in col.lower() or "_max" in col.lower():
            df[col] = df[col].astype(float)
        elif "_date" in col.lower() or "timestamp" in col.lower():
            df[col] = pd.to_datetime(df[col])
    return df

def make_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    print("{dir} created".format(dir=directory))

def rename_w_snowflake_column_naming_convention(df):
    df.columns = [x.upper().replace(" ","_") for x in df.columns]
    return df

def timeit(func, *args, **kwargs):
    import timeit
    def wrapper(func, *args, **kwargs):
        def wrapped():
            return func(*args, **kwargs)
        return wrapped
    wrapped = wrapper(func, *args, **kwargs)
    return timeit.timeit(wrapped, number=1)
