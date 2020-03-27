# -*- coding: utf-8 -*- 

"""Classes for S3 bucket."""

from mimetypes import guess_type
from botocore.exceptions import ClientError

class BucketManager:

    """Manage S3 Buckets."""
    
    def __init__(self, session):
        """Create a BucketManager object."""
        self.s3 = session.resource('s3')


    def all_buckets(self):
        """Get iterator for all buckets"""
        return self.s3.buckets.all()


    def all_objects(self, bucket_name):
        """Get iterator for objects in a bucket."""
        return self.s3.Bucket(bucket_name).objects.all()


    def create_bucket(self, bucket_name):
        s3bucket = None
        try:
            s3bucket = self.s3.create_bucket(
                Bucket=bucket_name
                # CreateBucketConfiguration=
                # {'LocationConstraint'= self.session.region_name}
            )
        except ClientError as error:
            if error.response['Error']['Code'] == 'BucketAlreadyExists':
                print("Bucket Name already in use")
            else:
                raise error
        return s3bucket


    def set_policy(self, bucket):
        policy = """{
            "Version":"2012-10-17",
            "Statement":[{
            "Sid":"PublicReadObject",
            "Effect":"Allow",
            "Principal":"*",
            "Action":["s3:GetObject"],
            "Resource":["arn:aws:s3:::%s/*"]
            }
            ]
        }""" % bucket.name
        pol = bucket.Policy()
        pol.put(Policy=policy)
    

    def configure_website():



