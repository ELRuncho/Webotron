import boto3
import click
session= boto3.Session(profile_name='sandbox')
s3 = session.resource('s3')

@click.group()
def cli():
    'Webotron uploads websites to AWS S3'
    pass

@cli.command('list-buckets')
def list_buckets():
    'Lists buckets'
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    "List of objects on a specified S3 Bucket"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)

if __name__ == "__main__":
    cli()