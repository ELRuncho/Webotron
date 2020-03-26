# -*- coding: utf-8 -*-
"""Webotron: Deploy websites to s3 buckets."""

from pathlib import Path
from mimetypes import guess_type
import boto3
from botocore.exceptions import ClientError
import click
from bucket import BucketManager

SESSION = boto3.Session(profile_name='sandbox')
bucket_manager = BucketManager(SESSION)
#s3 = SESSION.resource('s3')


def upload_file(s3bucket, path, key):
    """Upload path to s3 bucket at key."""
    content_type = guess_type(key)[0] or 'text/html'
    s3bucket.upload_file(
        path,
        key,
        ExtraArgs={
            'ContentType': content_type
        }
    )


@click.group()
def cli():
    """Webotron uploads websites to AWS S3."""


@cli.command('list-buckets')
def list_buckets():
    """List buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List of objects on a specified S3 Bucket."""
    for obj in bucket_manager.s3.Bucket(bucket).objects.all():
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and config s3 website."""
    try:
        s3bucket = bucket_manager.create_bucket(
            Bucket=bucket
            # CreateBucketConfiguration=
            # {'LocationConstraint'= SESSION.region_name}
        )
    except ClientError as error:
        if error.response['Error']['Code'] == 'BucketAlreadyExists':
            print("Bucket Name already in use")
        else:
            raise error

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
        }""" % s3bucket.name
    pol = s3bucket.Policy()
    pol.put(Policy=policy)
    webconfig = s3bucket.Website()
    webconfig.put(
        WebsiteConfiguration={
                        'ErrorDocument': {'Key': 'error.html'},
                        'IndexDocument': {'Suffix': 'index.html'}
        }
    )
    # url="http://%s.s3-website-us-east-1.amazonaws.com" % s3bucket.name


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync the contents of a given path to a Bucket."""
    s3bucket = bucket_manager.Bucket(bucket)
    root = Path(pathname).expanduser().resolve()

    def handle_directory(target):
        for path in target.iterdir():
            if path.is_dir():
                handle_directory(path)
            if path.is_file():
                upload_file(s3bucket, str(path), str(path.relative_to(root)))

    handle_directory(root)


if __name__ == "__main__":
    cli()
