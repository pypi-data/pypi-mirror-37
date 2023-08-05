#!/usr/bin/env python
import sys
import os
import boto3
import time
import vmtools
from awsretry import AWSRetry
import botohelper.route53 as route53
import botohelper.botohelpermain

vm_root_path = vmtools.vm_root_grabber()
sys.path.append(vm_root_path)
from local_settings import *

class S3(botohelper.botohelpermain.Main):
    """Class to manipulate aws ec2 resources

    public methods:

    instance variables:
    self.aws_profile
    self.aws_region
    self.session
    self.client_ec2
    self.ec2
    self.availability_zones_list
    self.route53
    """

    def __init__(self, aws_profile, aws_region):
        """set instance variables, set instance aws connections

        keyword arguments:
        :type aws_profile: string
        :param aws_profile: the profile to use from ~/.aws/credentials to connect to aws
        :type aws_region: string
        :param aws_region: the region to use for the aws connection object (all resources will be created in this region)
        """
        super().__init__(aws_profile=aws_profile, aws_region=aws_region)
        self.client_s3 = self.session.client('s3', region_name=self.aws_region)
        self.resource_s3 = self.session.resource('s3', region_name=self.aws_region)


    def get_matching_s3_objects(self, bucket, prefix='', suffix=''):
        """
        Return a generator of matching objects from an S3 bucket.
    
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        :type prefix: string or tuple
        :param prefix: (Optional) Only fetch objects whose key starts with
        :type suffix: string or tuple
        :param suffix: (Optional) Only fetch objects whose keys end with
        """
        kwargs = {'Bucket': bucket}
    
        # If the prefix is a single string (not a tuple of strings), we can
        # do the filtering directly in the S3 API.
        if isinstance(prefix, str):
            kwargs['Prefix'] = prefix
    
        while True:
    
            # The S3 API response is a large blob of metadata.
            # 'Contents' contains information about the listed objects.
            resp = self.client_s3.list_objects_v2(**kwargs)
    
            try:
                contents = resp['Contents']
            except KeyError:
                return
    
            for obj in contents:
                key = obj['Key']
                if key.startswith(prefix) and key.endswith(suffix):
                    yield obj
    
            # The S3 API is paginated, returning up to 1000 keys at a time.
            # Pass the continuation token into the next response, until we
            # reach the final page (when this field is missing).
            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break
    
    
    def get_matching_s3_keys(self, bucket, prefix='', suffix=''):
        """
        Generate the keys in an S3 bucket.
    
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        :type prefix: string or tuple
        :param prefix: (Optional) Only fetch objects whose key starts with
        :type suffix: string or tuple
        :param suffix: (Optional) Only fetch objects whose keys end with
        """
        for obj in self.get_matching_s3_objects(bucket, prefix, suffix):
            yield obj['Key']

    def download_s3_file(self, bucket, remote_file_to_download, local_absolute_path):
        """
        download the remote_file_to_download from s3 to local_absolute_path
    
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        :type remote_file_to_download: string
        :param remote_file_to_download: the key of the remote file to download from s3
        :type local_absolute_path: string
        :param local_absolute_path: the absolute path where to download remote_file_to_download
        """
        self.client_s3.download_file(bucket, remote_file_to_download, local_absolute_path)

    def request_restore_from_glacier(self, bucket, key, number_of_days):
        """
        Request a resotre from glaicer to s3 return the response
    
        :type bucket: string
        :param bucket: Name of the S3 bucket.
        :type key: string
        :param key: the key of the remote file to restore from glacier
        :type number_of_days: int
        :param number_of_days: the number of days you want to wait for the restore (the quickest would be 1 but a higher number will incur less cost)
        """
        bucket_obj = self.resource_s3.Bucket(bucket)
        object_summary_iterator = bucket_obj.objects.filter(Prefix=key)
        object_summary_list = []
        for object_summary in object_summary_iterator:
            object_summary_list.append(object_summary)
        if len(object_summary_list) == 0:
            return None
        elif len(object_summary_list) > 1:
            raise ValueError('object_summary_list should only have 1 or 0 object, key filter must not be specific enough')
        request_response = bucket_obj.meta.client.restore_object(Bucket=bucket, Key=key, RestoreRequest={'Days': number_of_days})
        return request_response



