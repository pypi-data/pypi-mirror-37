#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-24


from gagoos.s3 import S3StorageService
import boto3


class CephStorageService(S3StorageService):
    def __init__(
            self,
            auth_first: str,
            auth_second: str,
            region: str,
            proxies: dict = None
    ):
        super().__init__(
            auth_first,
            auth_second,
            region,
            proxies
        )
        self.client = boto3.client(
            's3',
            aws_access_key_id=auth_first,
            aws_secret_access_key=auth_second,
            endpoint_url=region,
        )


def create_service(
        first: str,
        second: str,
        region: str,
        proxies: dict = None
):
    return CephStorageService(
        first,
        second,
        region,
        proxies
    )
