# -*- coding: utf-8 -*- 

"""Classes for S3 bucket."""

class BucketManager:
    """Manage S3 Buckets."""
    def __init__(self, session):
        """Create a BucketManager object."""
        self.s3 = session.resource('s3')
    
    def all_buckets(self):
        """Get iterator for all buckets"""
        return self.s3.buckets.all()

    def all_objects(self, bucket):
        """Get iterator for objects in a bucket."""
        return self.s3.Bucket(bucket).objects.all()



