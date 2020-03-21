# coding: utf-8
import boto3
session= boto3.Session(profile_name='sandbox')
s3 = session.resource('s3)
s3 = session.resource('s3')
for bucket in s3.buckets.all():
    print(bucket)
    
get_ipython().run_line_magic('history', '')
