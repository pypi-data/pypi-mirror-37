import os
import logging
from logging import handlers


class CustomTimeRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, filename, header, when='midnight', interval=1, backupCount=0, encoding=None,
                 delay=False, utc=True, atTime=None):

        logging.handlers.TimedRotatingFileHandler.__init__(self, filename=filename, when=when,
                                                           interval=interval,
                                                  backupCount=backupCount, encoding=encoding, delay=delay,
                                                  utc=utc, atTime=atTime)
        self.file_pre_exists = os.path.exists(filename)
        self.header = header
        self.suffix = "%Y%m%d_%H%M"
        # Mandatory to make a rollover to write the header
        self.doRollover()

    def emit(self, record):
        # Call the parent class emit function.
        logging.handlers.TimedRotatingFileHandler.emit(self, record)

    def doRollover(self):
        logging.info("Rotating file...")
        logging.handlers.TimedRotatingFileHandler.doRollover(self)
        # Write header when file has rotated
        self.stream.write('{}\n'.format(self.header))