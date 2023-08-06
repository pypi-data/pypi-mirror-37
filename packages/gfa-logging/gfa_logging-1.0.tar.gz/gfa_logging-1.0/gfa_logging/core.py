"""
    A class to generate messages for debug logs or data
"""

import logging
from time import gmtime
from os import path, makedirs
from gfa_logging.custom_file_handler import CustomTimeRotatingFileHandler


class MsgLogger:
    """
    Message logger to debug the application

    :param debug_mode: used for the logger level
    :param logging_to_console: force the logging in the console when the process run in background
    :param log_path: absolute or relative path to the logs directory
    :param file_name: name of the log file
    :param max_bytes: size of the file
    :param backup_count: number of log to keep before erasing
    :param when: moment for the rollover (S for seconds, M for minutes, H for hours, D for days, midnight)
    :param interval: inverval for the rollover
    :param header: header to add at the top of the file
    :param date_formatter: add date and time in the log

    :type debug_mode: bool
    :type logging_to_console: bool
    :type log_path: str
    :type file_name: str
    :type max_bytes: int
    :type backup_count: int
    :type when: str
    :type interval: int
    :type header: str
    :type date_formatter: bool

    """
    def __init__(self, name='msg_logger', debug_mode=False, logging_to_console=False, log_path='logs',
                 file_name='msg_log', max_bytes=262144, backup_count=30, when='D', interval=1, header='',
                 date_formatter=False):
        self.name = name
        self.debug_mode = debug_mode
        self.logging_to_console = logging_to_console
        self.file_name = file_name
        self.log_path = log_path
        self.file_path = ''
        self.log_format = '%(asctime)-15s | %(process)d | %(levelname)s: %(message)s'
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.when = when
        self.interval = interval
        self.header = header
        self.logger = logging.getLogger(self.name)
        self.msg_handler = None
        self.formatter = logging.Formatter(self.log_format)
        self.date_formatter = date_formatter
        
        self.setup()

    def setup(self):
        if self.logging_to_console:
            self.logger.addHandler(logging.StreamHandler())

        # Debug logger setup
        if not path.exists(self.log_path):
            makedirs(self.log_path)
        self.file_path = path.join(self.log_path, self.file_name)
        self.msg_handler = CustomTimeRotatingFileHandler(self.file_path, header=self.header, when=self.when,
                                                         interval=self.interval)
        if self.date_formatter is True:
            self.formatter.converter = gmtime
            self.formatter.datefmt = '%Y/%m/%d %H:%M:%S UTC'
            self.msg_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.msg_handler)

        # Set logging
        if self.debug_mode is True:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)


if __name__ == "__main__":
    """Example with debug message logger and a data logger"""

    msg_logger = MsgLogger(debug_mode=True, date_formatter=True)
    data_logger = MsgLogger(name='data_logger', file_name='data', log_path='data', when='H',
                            header="sensorID,value,timestamp")

    msg_logger.logger.info('_____ Started _____')
    data_logger.logger.info("281868,28.5,1540476278")
