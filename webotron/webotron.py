import boto3
import click
from botocore.exceptions import ClientError

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

@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    "create and config s3 website"
    try:
        s3bucket=s3.create_bucket(
            Bucket=bucket
            #CreateBucketConfiguration={'LocationConstraint'= session.region_name} 
        )
    except ClientError as e:
        if e.response['Error']['Code']=='BucketAlreadyExists':
            print("Bucket Name already in use")
        else:
            raise e


    policy="""{
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
    webconfig=s3bucket.Website()
    webconfig.put(WebsiteConfiguration={'ErrorDocument':{'Key':'error.html'},'IndexDocument':{'Suffix':'index.html'}})
    #url="http://%s.s3-website-us-east-1.amazonaws.com" % s3bucket.name
    return





if __name__ == "__main__":
    cli()