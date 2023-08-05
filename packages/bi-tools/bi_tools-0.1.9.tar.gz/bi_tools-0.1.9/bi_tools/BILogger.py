from __future__ import print_function
import os
import os.path
import logging
import sys
import getpass
from datetime import datetime

class log_mode():
    critical = {"CRITICAL":40} #40 write to database, email, and text
    warning = {"WARNING":30} #30 write to database and email
    info = {"INFO":20} #20 write to database
    debug = {"DEBUG":10} #10 print
    notset = {"NOTSET":0} #0 nothing

# snowflake should have a schema called database Logs
# which should be split into different categories of logs
# for example, airflow dag, individual script

#TODO 1: make logger work both on vm and lm. 2: add feature for save to s3
class Logger(object):
    """Logger object for easier logging.

    Args:
        NA
    Returns:
        NA
    Raises:
        NA
    """
    def __init__(self, mode, exc_date=None):
        self.mode = getattr(log_mode, "critical").keys()[0]
        self.mode_score = getattr(log_mode, "critical").values()[0]
        self.username = getpass.getuser()
        self.run_file = os.path.basename(sys.argv[0]).replace(".py", "")
        if exc_date is  None:
            self.exc_date = str(datetime.today().date())
        else:
            self.exc_date = exc_date

        #set up the log files
        self._create_log_file()
        self._config()
        self._set_default_logs()
        self.execution_date()

    def _create_log_file(self):
        #if log directory does not exist, then create so we can write some logs
        log_directory = "/home/{}/logs".format(self.username)
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        log_path = "{}/{}_{}.log".format(log_directory,
            self.run_file,
            self.exc_date)
        if os.path.isfile(log_path):
            os.remove(log_path)
        self.logger = logging.getLogger(self.run_file)
        self.handler = logging.FileHandler(log_path)

    def print_log(self, msg):
        """Prints log if the log level exceeds the 'info' level.

        Args:
            msg: log message that you want to print
        Returns:
            NA
        Raises:
            NA
        """
        import sys
        if self.mode_score <= 20:
            print(msg)
        else:
            pass

    def _config(self):
        """Configures the logging settings.

        Args:
            NA
        Returns:
            NA
        Raises:
            NA
        """
        self.logger.setLevel(os.environ.get("LOGLEVEL", self.mode.upper()))
        self.handler.setLevel(os.environ.get("LOGLEVEL", self.mode.upper()))
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(format)
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)

    def custom_log(self, message):
        """Logs a custom message.

        Args:
            message: custom message for logging
        Returns:
            NA
        Raises:
            NA
        """
        self.print_log(message)
        self.logger.info(message)

    def execution_date(self):
        """Logs information about the execution date.

        Args:
            NA
        Returns:
            NA
        Raises:
            NA
        """
        self.print_log(self.execution_date_msg)
        self.logger.info(self.execution_date_msg)

    def ran_info(self):
        self.print_log("{} & {}".format(self.ran_by_msg, self.ran_when_msg))
        self.logger.info("{} & {}".format(self.ran_by_msg, self.ran_when_msg))
