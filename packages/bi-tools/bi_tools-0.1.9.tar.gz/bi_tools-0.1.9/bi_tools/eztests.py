import pandas as pd
from datetime import datetime, timedelta

def date_exists_in_db(date, conn, table_name, schema_name, date_var):
    exists = False
    print "checking data for the given date in the db"
    exc_date = str(date)[:10] #in the format of "2018-01-18"
    print exc_date
    query = """select * from {schema}.{table} WHERE
                trunc({date_var}) = '{date}' limit 5;"""\
                    .format(date=exc_date, schema=schema_name,
                            table=table_name, date_var=date_var)
    db_df = conn.sql_dataframe(query)

    if db_df.empty:
        exists = False
    else:
        exists = True

    return exists
