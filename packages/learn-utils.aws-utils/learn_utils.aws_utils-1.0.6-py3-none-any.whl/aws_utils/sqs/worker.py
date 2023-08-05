"""
Worker module - Defines the workers that performs the whole ingestion process.
"""
from aws_utils.sqs.consumer import Consumer
from aws_utils import aws_logger


class Worker(object):
    """
    Defines workers objects that performs the data-ingestion process 
    for the messages that are recovered from the 'aws.sqs' message queue.
    """
    def __init__(self, **kwargs):
        """
        Worker initialization function.
        :param **kwargs: a dictionary like object containing the system worker configurations.
        :param queue_name: **required** parameter containing the name of the 'aws.sqs' message queue.
        :param batch_size: number of messages that are receives by the worker.
                           
                           Default: 1
                           
        :param visibility_timeout: The length of time (in seconds) during which a message will be unavailable after a message 
                                   is delivered from the queue. 
                                   
                                   Default: 30
                                   
        :param wait_time: The duration (in seconds) for which the call waits for a message to arrive in the queue
                          before returning. If a message is available, the call returns sooner than WaitTimeSeconds. 
                          If no messages are available and the wait time expires,
                          the call returns successfully with an empty list of messages.
                          
                          Default: 60
        
        """
        queue_name = kwargs['queue_name'],
        batch_size = kwargs['batch_size'],
        visibility_timeout = kwargs['visibility_timeout'],
        wait_time = kwargs['wait_time']

        self._consumer = Consumer(
            queue_name=queue_name,
            batch_size=batch_size,
            visibility_timeout=visibility_timeout,
            wait_time=wait_time
        )
        self._consumer += self.load_data

    def load_data(self, message):
        """
        Loads the message data to the AML database.
        Loads data to the neo4j.
        :param message: a single message registered in the message queue.
        """
        try:
            # TODO: setup the callback function
            aws_logger.logger.warning(message.body)
        except Exception as ex:
            ex.__setattr__('queue_msg', str(message))
            aws_logger.logger.exception(
                str(ex),
                extra={'message.body':message.body, 'message.attributes':message.attributes}
            )
            raise ex

    def run(self):
        """
        Runs the ingestion consumer process.
        :return: 
        """
        try:
            while True:
                self._consumer.consume()
        except Exception as ex:
            if hasattr(ex,'queue_msg'):
                # if the exception has an attribute called 'queue_msg', then log it as extra information.
                aws_logger.logger.exception(
                    str(ex),
                    extra={
                        'queue_msg.body':ex.queue_msg.body,
                        'queue_msg.attributes':ex.queue_msg.attributes
                    }
                )
            else:
                # else log the exception without extra data.
                aws_logger.logger.exception(str(ex))
