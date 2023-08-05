import argparse
from datetime import datetime,timedelta

class Parser(object):
    """Parser object for easier system argument parsing.

    Args:
        NA
    Returns:
        NA
    Raises:
        NA
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(description=
            'Combines test_platform_logs with test_platform_logs_archive')
        self.exc_date, self.mode = self._arg_parser()

    def _arg_parser(self):
        """Parses the arguments.

        Args:
            NA
        Returns:
            NA
        Raises:
            NA
        """

        """
        DATE:
        '2018-06-08'

        LEVELS:
        CRITICAL	50
        ERROR	    40
        WARNING	    30
        INFO	    20
        DEBUG	    10
        NOTSET      0
        """
        today = [str(datetime.today().date())]
        self.parser.add_argument('-d', metavar='N',
                                type=str, nargs='+', default=today,
                                dest='exc_date', help="date of execution")
        self.parser.add_argument('-m', metavar='N',
                        type=str, nargs='+', default=["INFO"],
                        dest='mode', help="logging level")
        args = self.parser.parse_args()
        return args.exc_date[0], args.mode[0]
