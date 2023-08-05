#!/usr/bin/env python
# -*- coding: utf-8 -*-
# create by wanglin, at 2018.10.05, https://newops.cn

################ Tencent cos ##############
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import os
from urllib import unquote

class TencentCosVersions():
    def __init__(self, BUCKET, PREFIX, ARTIFACT_ID):
        self.BUCKET = BUCKET
        self.PREFIX = PREFIX
        self.ARTIFACT_ID = ARTIFACT_ID

    def get_versions(self):
        secret_id = os.environ.get('SECRET_ID')
        secret_key = os.environ.get('SECRET_KEY')
        region = os.environ.get('S3_REGION')

        if secret_id is None or secret_key is None or region is None:
            raise KeyError('No SECRET_ID or SECRET_KEY or S3_REGION found!')

        token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
        scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        # 2. 获取客户端对象
        client = CosS3Client(config)

        # 拼装"版本路径/工程名/"作为子串. 精确定位工程目录
        filter_str = self.PREFIX + '/' + self.ARTIFACT_ID + '/'
        response = client.list_objects(
            Bucket=self.BUCKET,
            Delimiter='/',
            Marker='',
            MaxKeys=1000,
            Prefix=filter_str,
            EncodingType='url'
        )

        #if not 'Contents' in response:
        #    raise KeyError('No ARTIFACT_ID directory found: ' + self.BUCKET + ':' + filter_str)

        if not 'CommonPrefixes' in response:
            raise KeyError('No SEMVER directory found in ' + self.BUCKET + ':' + filter_str)

        version_dirs = []
        for Prefix in response['CommonPrefixes']:
            Prefix_encode = Prefix['Prefix'].split('/')[-2]
            version_dirs.append(unquote(Prefix_encode))

        return version_dirs
