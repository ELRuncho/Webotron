import boto3
import click
session= boto3.Session(profile_name='sandbox')
s3 = session.resource('s3')

@click.command('list-buckets')
def list_buckets():
    'Lists buckets'
    for bucket in s3.buckets.all():
        print(bucket)


if __name__ == "__main__":
    list_buckets()