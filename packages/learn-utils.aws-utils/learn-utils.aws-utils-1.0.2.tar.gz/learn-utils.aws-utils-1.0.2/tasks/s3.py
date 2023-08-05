# -*- coding: utf-8 -*-
"""
module s3.py:
---------------
Automates complex sequences of s3 commands via a single application command.
"""
from invoke import task
import boto3

#tasks definitions

# s3 bucket name used by this test suite
bucket_name = "s3client.bucket.test"
# endoint url used by this test suite
endpoint_url = 'http://localstack:4572'


@task
def create_buckets(context):
    """A tasks that creates aws.s3.buket
    """
    s3 = boto3.resource(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id="secretkey",
        aws_secret_access_key="accesskey",
        region_name='us-east-1', verify=False
    )
    s3.create_bucket(Bucket=bucket_name)

@task
def delete_buckets(context):
    """A tasks that creates aws.s3.buket
    """
    s3 = boto3.resource(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id="secretkey",
        aws_secret_access_key="accesskey",
        region_name='us-east-1', verify=False
    )
    for bucket in s3.buckets.all():
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

@task
def delete_all_files(context):
    s3 = boto3.resource(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id="secretkey",
        aws_secret_access_key="accesskey",
        region_name='us-east-1', verify=False
    )
    for bucket in s3.buckets.all():
        for key in bucket.objects.all():
            key.delete()

@task
def print_all_files(context):
    s3 = boto3.resource(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id="secretkey",
        aws_secret_access_key="accesskey",
        region_name='us-east-1', verify=False
    )
    for bucket in s3.buckets.all():
        for key in bucket.objects.all():
            print(key)