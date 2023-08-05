import sys
import logging
import datetime
import watchtower
import boto3
import botocore
import time


class AWSLogger(logging.Logger):
    log_format = "%(asctime)s [%(filename)s] [%(funcName)s] [%(levelname)s] [%(lineno)d] %(message)s"
    formatter = logging.Formatter(log_format)

    def __init__(self, pid):
        logger_name = "{}_worker_{}".format(datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f"), pid)
        super().__init__(name=logger_name)

        self.addHandler(AWSLogger.get_stream_handler_instance())

    def add_watchtower_handler(self, log_group):
        self.addHandler(AWSLogger.get_cloudwatch_handler_instance(log_group))

    @staticmethod
    def get_stream_handler_instance():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(AWSLogger.formatter)
        return console_handler

    @staticmethod
    def get_cloudwatch_handler_instance(log_group):
        try:
            cloudwatch_handler = watchtower.CloudWatchLogHandler(log_group=log_group,
                                                                 boto3_session=boto3.Session(region_name='sa-east-1'))
            cloudwatch_handler.setFormatter(AWSLogger.formatter)
            return cloudwatch_handler
        except botocore.errorfactory.OperationAbortedException:
            time.sleep(3)
            return AWSLogger.get_cloudwatch_handler_instance(log_group)

# logger instance
logger = None


def init(pid, log_group):
    """
    Logger initialization function. 
    This function is called from the flask-manager commands to initialize the log instance. 
    :param pid: WSGI process_id
    """
    import os
    global logger
    logger = AWSLogger(pid)
    tripod_config = os.getenv("TRIPOD_APP_CONFIG", "development")
    stream_logs_disable = os.getenv("STREAM_LOGS_DISABLE", False)
    if tripod_config == 'production' or (not stream_logs_disable and tripod_config == 'test'):
        logger.add_watchtower_handler(log_group)