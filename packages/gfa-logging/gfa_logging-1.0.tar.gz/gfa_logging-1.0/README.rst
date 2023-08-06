GFA Logging
===========

This library provide a logging class to record data or debug your application.



To install::

    python3 setup.py

Usage example for two loggers::

    from gfa_logging import MsgLogger

    msg_logger = MsgLogger()
    data_logger = MsgLogger(name='data_logger', file_name='data.csv',
                            header="sensorID,value,timestamp")

    msg_logger.logger.info('_____ Started _____')
    data_logger.logger.info("281868,28.5,1540476278")

