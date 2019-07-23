import boto3
from botocore.exceptions import ClientError
import logging

from django.conf import settings


class S3BucketServices:
    """        This Class Is Use To Handle All Functions In The Class By Importing It      """

    def __init__(self):
        self.access_key = settings.AWS_ACCESS_KEY_ID
        self.secret_key = settings.AWS_SECRET_ACCESS_KEY
        self.s3 = boto3.client('s3')
        self.default_bucket = "profiles3-assets"

    def bucket_exists(self, bucket_name):
        try:
            self.s3.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            logging.debug(e)
            return False
        return True

    def create_bucket(self, bucket_name, region=None):
        try:
            if region is None:
                region = 'ap-south-1'
            if not self.bucket_exists(bucket_name):
                if region is None:
                    self.s3.create_bucket(Bucket=bucket_name)
                    print(bucket_name)
                else:
                    s3_client = boto3.client('s3', region_name=region)
                    location = {'LocationConstraint': region}
                    s3_client.create_bucket(Bucket=bucket_name,
                                            CreateBucketConfiguration=location)
            else:
                print("Already Exist..")
                return False
        except ClientError as e:
            logging.error(e)
            print("Bucket Already Exist")
            return False
        return True


def delete_bucket(bucket_name):
    """Delete an empty S3 bucket
    If the bucket is not empty, the operation fails.
    :param bucket_name: string
    :return: True if the referenced bucket was deleted, otherwise False
    """

    # Delete the bucket
    s3 = boto3.client('s3')
    try:
        s3.delete_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_file(self, file, bucket_name, file_name):
    try:
        # print(file_name)
        self.s3.put_object(Bucket=bucket_name, Key=file_name, Body=file)
    except ValueError as e:
        print(e)
        return False
    return True


def getfile(self, bucket_name, object_name):
    try:
        response = self.s3.get_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        # AllAccessDisabled error == bucket or object not found
        logging.error(e)
        return None
    # Return an open StreamingBody object
    return response['Body']


def deletefile(self, bucketname, filename):
    try:
        self.s3.delete_object(Bucket=bucketname, Key=filename)
    except ClientError as e:
        logging.error(e)
        return False
    return True
