"""
module s3_client.py
----------------------
| An S3-client module.
| Provides classes and functions to interact with an S3-buckets.
"""
import boto3
import os
from io import BytesIO
import botocore


class S3Client(object):
    """
    A simple S3 client class to interact with an amazon s3 Bucket
    """

    def __init__(self, bucket, endpoint_url=None):
        """
        S3 Client initializer
        :param bucket: the name of the bucket in a s3 server
        :param endpoint_url: s3 endpoint url to be used. 
        *DEFAULT*=None
        If default value boto3 will resolve the url endpoint and send all requests to the aws.
        :type bucket: str
        """
        self.bucket_name = bucket
        self.s3 = boto3.resource('s3', endpoint_url=endpoint_url)
        self.bucket = self.s3.Bucket(self.bucket_name)
        self.exists = True
        try:
            self.s3.meta.client.head_bucket(Bucket=self.bucket_name)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                exists = False

    def upload_file(self, file_name, bfile, base_path=None):
        """
        A method of S3 Client class to upload files to the S3 bucket
        :param filename: name of the file
        :type filename: str
        :param bfile: the content of the file
        :type bfile: bytes
        :param basepath: path to the file
        :type basepath: str
        """
        if base_path is not None:
            file_name = os.path.join(base_path, file_name)
        with BytesIO(bfile) as f:
            self.bucket.upload_fileobj(Fileobj=f, Key=file_name)

    def list_files(self):
        """
        A method of S3 Client class to get all files in the S3 Bucket
        :return: list of files
        """

        files_list = list()
        for key in self.bucket.objects.all():
            files_list.append(key.key)

        return files_list

    def delete_files(self,file_list):
        """
        A method of S3 Client class to the delete files in the S3 Bucket
        :param file_list: List of files to be deleted
        :type  file_list: list
        """
        for file in file_list:
            obj = self.s3.Object(bucket_name=self.bucket_name, key=file)
            obj.delete()

    def download_files(self, file_names):
        """Downloads a set of files from the S3-Bucket.
        Downloads files from the S3_Bucket and returns them as byte array.
        :param file_names: an list of file names.
        :return: a list of byte arrays representing the files content.
        """
        file_list = list()
        for f in file_names:
            with BytesIO() as writter:
                self.bucket.download_fileobj(f, writter)
                file_list.append(writter.getvalue())
        return file_list

    def download_file(self, file_name):
        """Downloads an file from the S3-Bucket.
        Downloads an file from the S3_Bucket and returns it as bytearray.
        :param file_name: a file name.
        :type file_name: str
        :return: an byte array representing the file content.
        """
        with BytesIO() as writter:
            self.bucket.download_fileobj(file_name, writter)

            return writter.getvalue()