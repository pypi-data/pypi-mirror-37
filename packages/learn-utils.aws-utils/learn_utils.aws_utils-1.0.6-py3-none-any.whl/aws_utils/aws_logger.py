import sys
import logging
import datetime
from watchtower import CloudWatchLogHandler as BaseHandler
import watchtower
import boto3
import time
from botocore.exceptions import ClientError


class CloudWatchLogHandler(BaseHandler):

    def __init__(self, client, log_group=__name__, stream_name=None, use_queues=True, send_interval=60,
                 max_batch_size=1024*1024, max_batch_count=10000, create_log_group=True, *args, **kwargs):
        watchtower.handler_base_class.__init__(self, *args, **kwargs)
        self.log_group = log_group
        self.stream_name = stream_name
        self.use_queues = use_queues
        self.send_interval = send_interval
        self.max_batch_size = max_batch_size
        self.max_batch_count = max_batch_count
        self.queues, self.sequence_tokens = {}, {}
        self.threads = []
        self.shutting_down = False
        self.cwl_client = client
        if create_log_group:
            watchtower._idempotent_create(
                self.cwl_client.create_log_group,
                logGroupName=self.log_group
            )


class AWSLogger(logging.Logger):

    def __init__(self, logger_name, log_group, region,
                 aws_access_key_id=None, aws_secret_access_key=None, endpoint_url=None,
                 aws_session_token=None, should_add_watchtower=True):
        self.log_format = "%(asctime)s [%(filename)s] [%(funcName)s] [%(levelname)s] [%(lineno)d] %(message)s"
        self.formatter = logging.Formatter(self.log_format)

        self.log_group = log_group
        self.region = region

        super().__init__(name=logger_name)

        self.addHandler(self.get_stream_handler_instance())

        if should_add_watchtower:
            self.client = boto3.client(
                'logs',
                region_name=self.region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                aws_session_token=aws_session_token,
                endpoint_url=endpoint_url
            )
            self.add_watchtower_handler()

    def add_watchtower_handler(self):
        self.addHandler(self.get_cloudwatch_handler_instance())

    def get_stream_handler_instance(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    def get_cloudwatch_handler_instance(self):
        try:
            cloudwatch_handler = CloudWatchLogHandler(
                client=self.client,
                log_group=self.log_group,
            )
            cloudwatch_handler.setFormatter(self.formatter)
            return cloudwatch_handler
        except ClientError:
            time.sleep(3)
            return AWSLogger.get_cloudwatch_handler_instance(self.log_group)
