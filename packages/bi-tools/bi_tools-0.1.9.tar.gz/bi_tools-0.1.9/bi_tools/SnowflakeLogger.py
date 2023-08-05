from BILogger import Logger
from datetime import datetime

class SnowflakeLogger(Logger):
    def __init__(self, schema_name, table_name, **kwargs):
        if "bucket_name" in kwargs:
            self.bucket_name = kwargs["bucket_name"]
        else:
            self.bucket_name = "pitchbook-snowflake"
        self.schema_name = schema_name.upper()
        self.table_name = table_name.upper()
        self.today = datetime.strftime(datetime.today(), "%Y-%m-%d")
        Logger.__init__(self, mode="debug", exc_date=None)

    def move_log_to_s3(self):

    def _create_log_file(self):
        #if log directory does not exist, then create so we can write some logs
        log_directory = "s3://{bucket}/schema={schema}/table={table}/".format(
            bucket=self.bucket_name,
            schema=self.schema_name,
            table=self.table_name
        )
        log_path = "{}/{}_{}.log".format(log_directory,
            self.schema_name,
            self.table_name)
        if os.path.isfile(log_path):
            os.remove(log_path)
        self.logger = logging.getLogger("SNOWFLAKE_LOG")
        self.handler = logging.FileHandler(log_path)
