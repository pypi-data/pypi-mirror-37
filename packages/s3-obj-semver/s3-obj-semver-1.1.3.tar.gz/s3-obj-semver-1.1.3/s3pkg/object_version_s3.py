#!/usr/bin/env python
# -*- coding: utf-8 -*-
# create by wanglin, at 2018.01.23, https://newops.cn

################ AWS s3 ##############
#from semver_max import semver_max
import boto3
import botocore
from log import logger as log
from urllib import unquote

class AwsS3Versions():
    def __init__(self, BUCKET, PREFIX, ARTIFACT_ID):
        self.BUCKET = BUCKET
        self.PREFIX = PREFIX
        self.ARTIFACT_ID = ARTIFACT_ID

    def get_versions(self):
        # defautl connect_timeout is 60s, max_attempts is 4
        # https://boto3.readthedocs.io/en/latest/reference/core/session.html#boto3.session.Session.resource
        #s3 = boto3.resource('s3', config=botocore.config.Config(connect_timeout=10, retries={'max_attempts': 3}))
        #bucket = s3.Bucket(self.BUCKET)
        
        #for key in bucket.objects.all():
            #print(key.key)
        
        #version_dirs = []
        # 拼装"版本路径/工程名/"作为子串. 精确定位工程目录
        filter_str = self.PREFIX + '/' + self.ARTIFACT_ID + '/'

        #for obj in bucket.objects.filter(Delimiter='', Prefix=filter_str):
        #    log.info('{0}:{1}'.format(bucket.name, obj.key))
        #    # 取工程目录下的所有文件或目录
        #    last_str = obj.key.split(filter_str)[-1]
        #    # 去除文件
        #    if '/' in last_str:
        #        # 获取版本号
        #        version = last_str.split('/')[0]
        #        #log.debug('last_str: {0}, version: {1}'.format(last_str, version))
        #        if version is not None:
        #            version_dirs.append(version)

        #response = bucket.objects.filter(Delimiter='/', Prefix=filter_str)

        client = boto3.client('s3')

        response = client.list_objects(
            Bucket=self.BUCKET,
            Delimiter='/',
            EncodingType='url',
            Marker='',
            MaxKeys=100,
            Prefix=filter_str,
            RequestPayer='requester'
        )

        #if not 'Contents' in response:
        #    raise KeyError('No ARTIFACT_ID directory found: ' + self.BUCKET + ':' + filter_str)

        if not 'CommonPrefixes' in response:
            raise KeyError('No SEMVER directory found in ' + self.BUCKET + ':' + filter_str)

        version_dirs = []
        for Prefix in response['CommonPrefixes']:
            Prefix_raw = Prefix['Prefix'].split('/')[-2]
            version_dirs.append(unquote(Prefix_raw))

        return version_dirs
