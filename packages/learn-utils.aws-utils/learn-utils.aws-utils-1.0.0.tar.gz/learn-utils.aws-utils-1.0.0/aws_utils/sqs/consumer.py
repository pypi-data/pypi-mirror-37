"""
consumer module - Defines class and methods that handle with the 'aws.sqs' message queue.

    The current module a simple class that implements the consumer part of the producer/consumer pattern.
    
    The producer is responsible for creating/building messages (or tasks) that are published on the message queue.
    And the consumer is responsible for consuming messages (or tasks) from the message queue.
"""
import boto3
from collections import Iterable


class Consumer(object):
    """
    Consumer class defines consumer objects that are able to consume messages from the 'aws.sqs' message queue 
    and process them. 
    """

    def __init__(self, queue_name, **kwargs):
        """
        Consumer class initialization
        :param queue_name: a string representing the queue name.
        :param batch_size: the number of messages to retrieve from the message queue.
        :param visibility_timeout: the time in seconds that a message, retrieved from the queue, 
        will not from other workers.
        :param wait_time: time in seconds to wait until a message be available to be consumed.
        :param action_list: list of functions that produce new messages to the message queue.
        """
        self._sqs = boto3.resource("sqs")
        self._queue = self._sqs.get_queue_by_name(QueueName=queue_name)

        if 'batch_size' in kwargs:
            self._batch_size = kwargs['batch_size']
        else:
            self._batch_size = 100

        if 'visibility_timeout' in kwargs:
            self._visibility_timeout = kwargs['visibility_timeout']
        else:
            self._visibility_timeout = 30

        if 'wait_time' in kwargs:
            self._wait_time = kwargs['wait_time']
        else:
            self._wait_time = 60

        if 'action_list' in kwargs:
            self._actions = kwargs['action_list']
        else:
            self._actions = list()

    def __iadd__(self, action):
        """
        Appends an action to the action list.
        :param action: action function that receives a sqs message as parameter.
        """
        if callable(action):
            self._actions.append(action)
        elif isinstance(action, (list,tuple,Iterable)):
            self._actions.extend(action)
        else:
            raise ValueError("Action must be a callable object or a iterable.")
        return self

    def consume(self):
        """
        Receives messages and process them with the registered actions.
        """
        messages = self._queue.receive_messages(
            MaxNumberOfMessages=self._batch_size,
            VisibilityTimeout=self._visibility_timeout,
            WaitTimeSeconds=self._wait_time,
        )

        for message in messages:
            for action in self._actions:
                action(message)

            # Let the queue know that the message is processed
            message.delete()
