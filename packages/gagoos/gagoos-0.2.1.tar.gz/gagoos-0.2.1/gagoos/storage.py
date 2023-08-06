#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-06-13

from importlib import import_module
from sys import modules
from datetime import datetime
import shutil
import os
from uuid import uuid4


class GagoStorageError(Exception):
    pass


class BucketNotExistsError(GagoStorageError):
    pass


class ObjectExistsError(GagoStorageError):
    pass


class ObjectNotExistsError(GagoStorageError):
    pass


class ACLError(GagoStorageError):
    pass


class Object:
    def __init__(self, bucket_name: str, object_name: str, size: int, e_tag: str, last_modified: datetime):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.size = size
        self.e_tag = e_tag
        self.last_modified = last_modified

    def download_to_file(
            self,
            local_file_path: str,
            overwrite_if_exists: bool=True,
            requester_pay=False
    ):
        if not os.path.exists(local_file_path) or overwrite_if_exists:
            directory, file_name = os.path.split(local_file_path)
            temp_file_path = os.path.join(directory, str(uuid4()))
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            self._download_to_file(temp_file_path, requester_pay)
            if os.path.exists(local_file_path):
                os.remove(local_file_path)
            shutil.move(temp_file_path, local_file_path)
        else:
            raise FileExistsError

    def get_data(self, requester_pay: bool = False) -> bytes or None:
        pass

    def _download_to_file(self, local_file_path: str, requester_pay: bool = False):
        pass

    def get_url(self):
        pass

    def get_gdal_url(self):
        return '/vsicurl/%s' % (self.get_url(),)


class Bucket:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name

    def get_object_list(self, prefix: str=None, requester_pay=False) -> list:
        pass

    def get_object(self, object_name: str, requester_pay=False) -> Object or None:
        pass

    def get_object_data(self, object_name: str, requester_pay=False) -> bytes or None:
        pass

    def upload_file(self, local_file_path: str, object_name: str, acl: str, overwrite_if_exists: bool=True) -> Object:
        pass

    def upload_data(self, data: bytes, object_name: str, acl: str, overwrite_if_exists: bool=True) -> Object:
        pass

    def exist(self, object_name: str) -> bool:
        pass

    def remove(self, object_name: str):
        pass

    def batch_remove(self, object_names: list):
        pass

    def rename(self, object_name: str, new_object_name: str, acl: str='private'):
        pass


class StorageService:
    """
    a storage service provider abstract class
    """
    def __init__(self, auth_first: str, auth_second: str, proxies: dict = None):
        self.auth_first = auth_first
        self.auth_second = auth_second
        self.bucket = None
        self.proxies = proxies

    def get_bucket(self, bucket_name: str) -> Bucket:
        if self.bucket is None or self.bucket.bucket_name != bucket_name:
            self.bucket = self._get_bucket_impl(bucket_name)
        return self.bucket

    def _get_bucket_impl(self, bucket_name: str) -> Bucket:
        pass

    def get_object(self, bucket_name: str, object_name: str, requester_pay=False) -> Object or None:
        bucket: Bucket = self.get_bucket(bucket_name)
        return bucket.get_object(object_name, requester_pay)

    def get_data(self, bucket_name: str, object_name: str, requester_pay=False) -> bytes or None:
        bucket: Bucket = self.get_bucket(bucket_name)
        return bucket.get_object_data(object_name, requester_pay)

    def get_data_as_text(self, bucket_name: str, object_name: str, requester_pay=False, encoding='utf-8'):
        raw_data: bytes = self.get_data(bucket_name, object_name, requester_pay)
        if raw_data:
            return raw_data.decode(encoding)
        return None

    def get_object_list(self, bucket_name: str, prefix: str=None, requester_pay=False) -> list:
        bucket: Bucket = self.get_bucket(bucket_name)
        return bucket.get_object_list(prefix, requester_pay)

    def upload_file(self, bucket_name: str, object_name: str, local_file_path: str, acl: str='private',
                    overwrite_if_exists: bool=True) -> Object:
        """
        upload a file to object storage
        :param bucket_name: bucket name
        :param object_name: object name
        :param local_file_path: local file path
        :param acl: access control level, one of 'private'|'public-read'|'public-read-write'|'authenticated-read'
        :param overwrite_if_exists: indicates if overwrite the object when object already exists
        :return:
        """
        bucket: Bucket = self.get_bucket(bucket_name)
        return bucket.upload_file(local_file_path, object_name, acl, overwrite_if_exists)

    def upload_data(self, bucket_name, object_name: str, data: bytes, acl: str='private',
                    overwrite_if_exists: bool=True) -> Object:
        bucket: Bucket = self.get_bucket(bucket_name)
        return bucket.upload_data(data, object_name, acl, overwrite_if_exists)

    def download_object(self, bucket_name: str, object_name: str, local_file_path: str, overwrite_if_exists: bool=True):
        bucket: Bucket = self.get_bucket(bucket_name)
        obj: Object = bucket.get_object(object_name)
        obj.download_to_file(local_file_path, overwrite_if_exists)

    def exist(self, bucket_name: str, object_name: str) -> bool:
        bucket: Bucket = self.get_bucket(bucket_name)
        return bucket.exist(object_name)

    def remove(self, bucket_name: str, object_name: str):
        bucket: Bucket = self.get_bucket(bucket_name)
        bucket.remove(object_name)

    def batch_remove(self, bucket_name: str, object_names: list):
        bucket: Bucket = self.get_bucket(bucket_name)
        bucket.batch_remove(object_names)

    def rename(self, bucket_name: str, object_name: str, new_object_name: str, acl: str='private'):
        bucket: Bucket = self.get_bucket(bucket_name)
        bucket.rename(object_name, new_object_name, acl)


def create_service(
        provider_name: str,
        auth_first: str,
        auth_second: str,
        region: str,
        proxies: dict = None,
) -> StorageService:
    """
    create a service
    :param provider_name: s3, azure, aliyun, cephrgw
    :param auth_first: first param
    :param auth_second: second param
    :param region: region name for s3, oss or end point url for Azure Blob
    :param proxies: proxies for storage
    :return: StorageService
    """
    if __package__ is None:
        module_name = provider_name
        import_module(module_name)
        m = modules[module_name]
    else:
        module_name: str = '.' + provider_name
        import_module(module_name, package=__package__)
        m = modules[__package__ + "." + provider_name]
    if hasattr(m, 'create_service'):
        return m.create_service(auth_first, auth_second, region, proxies)


def create_service_from_config(config: dict) -> StorageService or None:
    """
    Create service from a config object, which has a structure below
    {
        'service': 'fs/s3/oss/ceph'
        ),
        'access_key': 'access key'
        ),
        'secret_key': 'secret key'
        ),
        'region': 'region name or root directory for fs'
        ),
        'proxies': {
            'http': 'http(s)://ip:port',
            'https': 'http(s)://ip:port'
        }
    }
    """
    if 'service' not in config \
            or 'access_key' not in config \
            or 'secret_key' not in config \
            or 'region' not in config:
        raise KeyError('Insufficient parameters given')
    if 'proxies' in config:
        proxies = config['proxies']
        if 'http' not in proxies and 'https' not in proxies:
            raise KeyError(
                'Proxies config must have either "http" or "https"'
            )
    else:
        proxies = None

    return create_service(
        config['service'],
        config['access_key'],
        config['secret_key'],
        config['region'],
        proxies
    )

if __name__ == '__main__':
    service: StorageService = create_service('s3', 'AKIAPZKG6ANJSGGNTDSQ', 'UUNXCjb3KNiJp0rpEN9qDi02Oj73Xf5STLdaQKmo',
                                             'cn-north-1')
    dd = 1
