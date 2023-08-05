"""
producer module - Defines class and methods that handle with the 'aws.sqs' message queue.

    The current module defines a class that implements the producer module of the producer/consumer pattern.
    
    The producer is responsible for creating/building messages (or tasks) that are published on the message queue.
    And the consumer is responsible for consuming messages (or tasks) from the message queue.
"""
import boto3
from collections import Iterable


class Producer(object):
    """
    Producer class defines the producer objects that are able to produce messages and send them
    to the 'aws.sqs' message queue.
    """
    def __init__(self, queue_name, **kwargs):
        """
        Consumer class initialization
        :param queue_name: a string representing the queue name.
        :param batch_size: the number of messages to retrieve from the message queue.
        :param action_list: list of functions that produce new messages to the message queue.
        """
        self._sqs = boto3.resource("sqs")
        self._queue = self._sqs.get_queue_by_name(QueueName=queue_name)
        if 'action_list' in kwargs:
            self._actions = kwargs['action_list']
        else:
            self._actions = list()
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

    def enqueue(self, body, attributes=None):
        """
        Enqueue a message to the sqs.
        :param body: the message body.
        :param attributes: message attributes.
            Each message attribute consists of a Name , Type , and Value.

            Name , type , value and the message body must not be empty or null.
            All parts of the message attribute, including Name , Type , and Value ,
            are part of the message size restriction (256 KB or 262,144 bytes).
            Allowed types:
                - StringValue (string)
                - BinaryValue (bytes)
                - DataType (string) -- [REQUIRED]
            Amazon SQS supports the following logical data types: String , Number , and Binary .
            For the Number data type, you must use StringValue .
            Refer http://boto3.readthedocs.io/en/latest/reference/services/sqs.html#SQS.Queue.send_message for more
            information.
        :returns ??
        """
        if attributes is None:
            response = self._queue.send_message(
                MessageBody=body,
            )
        else:
            response = self._queue.send_message(
                MessageBody=body,
                MessageAttributes=attributes
            )

    def enqueue_batch(self, entries):
        """
        Enqueue a set of messages to the sqs.
        :param entries: list of messages that are encoded in a dictionary.
        :returns ??
        """
        response = self._queue.send_messages(Entries=entries)

    def produce(self, inputs, *args, **kwargs):
        """
        Produces messages to be sent to the message queue.
        :param inputs: object input value.
        :param args: list of additional arguments.
        :param kwargs: dictionary mapping names to additional arguments.
        """

        for action in self._actions:
            result = action(inputs, args, kwargs)
            self.enqueue(**result)