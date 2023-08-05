#!/usr/bin/env python
# -*- coding: utf-8 -*-
# create by wanglin, at 2018.10.08, https://newops.cn

################ semver max ##############
import os
from log import logger as log
from semver_max import semver_max

def main():
    PROVIDER = os.environ['S3_PROVIDER']
    BUCKET = os.environ['S3_BUCKET']
    PREFIX = os.environ['S3_PREFIX']
    ARTIFACT_ID = os.environ['S3_ARTIFACT_ID']

    log.info("%s://%s/%s/%s" % (PROVIDER, BUCKET, PREFIX, ARTIFACT_ID))

    if PROVIDER == "s3":
        from object_version_s3 import AwsS3Versions as S3Versions
    elif PROVIDER == "cos":
        from object_version_cos import TencentCosVersions as S3Versions
    else:
        from object_version_minio import MinioVersions as S3Versions

    av = S3Versions(BUCKET, PREFIX, ARTIFACT_ID)
    sv = semver_max()

    S3PKG_VERSION = sv.find_version(None, av.get_versions())
    if S3PKG_VERSION is None:
        raise RuntimeError("No versioned directory found!")
    else:
        print("S3PKG_VERSION=" + str(S3PKG_VERSION))

if __name__ == "__main__":
    main()
