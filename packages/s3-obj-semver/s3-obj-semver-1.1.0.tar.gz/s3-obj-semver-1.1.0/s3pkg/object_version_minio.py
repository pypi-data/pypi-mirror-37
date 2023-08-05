#!/usr/bin/env python
# -*- coding: utf-8 -*-
# create by wanglin, at 2018.10.05, https://newops.cn

################ Tencent cos ##############
from minio import Minio
import os
from log import logger as log

class MinioVersions():
    def __init__(self, BUCKET, PREFIX, ARTIFACT_ID):
        self.BUCKET = BUCKET
        self.PREFIX = PREFIX
        self.ARTIFACT_ID = ARTIFACT_ID

    def get_versions(self):
        secret_id = os.environ.get('SECRET_ID')
        secret_key = os.environ.get('SECRET_KEY')
        endpoint = os.environ.get('S3_ENDPOINT')

        client = Minio(endpoint,
                       access_key=secret_id,
                       secret_key=secret_key)
        
        # List all object paths in bucket that begin with my-prefixname.
        filter_str = self.PREFIX + '/' + self.ARTIFACT_ID + '/'

        objects = client.list_objects(self.BUCKET, 
            prefix=filter_str,
            recursive=False
        )

        version_dirs = []
        count = 0
        for obj in objects:
            if not obj.object_name.encode('utf-8') == filter_str:
                Prefix_raw = obj.object_name.encode('utf-8').split('/')[-2]
                version_dirs.append(Prefix_raw)

            count += 1
            log.debug("semver dir: " + obj.bucket_name + " - " + obj.object_name.encode('utf-8') + " - count " + str(count))

        if not version_dirs:
            raise KeyError('No SEMVER directory found in ' + self.BUCKET + ':' + filter_str)

        return version_dirs
