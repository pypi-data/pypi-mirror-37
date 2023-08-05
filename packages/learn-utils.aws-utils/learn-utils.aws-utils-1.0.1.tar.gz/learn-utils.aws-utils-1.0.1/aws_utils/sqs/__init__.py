"""
sqs module - Defines class and methods that handle with the 'aws.sqs' message queue.

    The current module defines two simple classes that implements the producer/consumer pattern.

    The producer is responsible for creating/building messages (or tasks) that are published on the message queue.
    And the consumer is responsible for consuming messages (or tasks) from the message queue.
"""
from aws_utils.src.sqs.producer import Producer
