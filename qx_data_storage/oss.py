"""
Django Settings Config:

    QX_DATA_STORAGE_SETTINGS = {
        "ALIYUN_OSS": {
            "DOMAIN": "",
            "ENDPOINT": "",
            "BUCKET_NAME": "",
        },
    }
"""
import logging
import os
import six
import oss2
from urllib import parse
from django.utils.encoding import force_str
from django.conf import settings
from .django_oss_storage.backends import OssStorage

logger = logging.getLogger(__name__)


class BackendOssStorage(OssStorage):

    def __init__(self, access_key_id=None,
                 access_key_secret=None,
                 end_point=None,
                 bucket_name=None,
                 path="/backend"):
        self.OSS = settings.QX_DATA_STORAGE_SETTINGS['ALIYUN_OSS']
        access_key_id = access_key_id or self.OSS['ACCESS_KEY_ID']
        access_key_secret = access_key_secret or self.OSS['ACCESS_KEY_SECRET']
        end_point = end_point or self.OSS.get('ENDPOINT')
        bucket_name = bucket_name or self.OSS.get('BUCKET_NAME')
        self.location = path

        super().__init__(
            access_key_id, access_key_secret, end_point, bucket_name)

    def url(self, name, expire=24 * 60 * 60):
        if not name or name.startswith("http"):
            return name
        key = self._get_key_name(name)
        return parse.urljoin(self.OSS['DOMAIN'], key)

    def _save(self, name, content):
        target_name = self._get_key_name(name)
        full_name = self._full_name(name)
        logger.debug("target name: %s", target_name)
        logger.debug("content: %s", content)
        self.bucket.put_object(target_name, content)
        return os.path.normpath(full_name)

    def _full_name(self, name):
        return "/" + self._get_key_name(name)

    def _get_key_name(self, name):
        base_path = force_str(self.location)
        if name.startswith(base_path):
            return name
        final_path = parse.urljoin(base_path + "/", name)
        name = os.path.normpath(final_path.lstrip('/'))

        if six.PY2:
            name = name.encode('utf-8')
        return name


class AutoOssStorage():

    def __init__(self, appid=None,
                 appsecret=None,
                 bucket_name=None):
        self.OSS = settings.QX_DATA_STORAGE_SETTINGS['ALIYUN_OSS']
        appid = appid or self.OSS['ACCESS_KEY_ID']
        appsecret = appsecret or self.OSS['ACCESS_KEY_SECRET']
        bucket_name = bucket_name or self.OSS.get('BUCKET_NAME')
        auth = oss2.Auth(appid, appsecret)
        self.bucket = oss2.Bucket(
            auth, 'https://{}'.format(self.OSS.get('ENDPOINT')),
            bucket_name)

    def put_bytes(self, name: str, data: bytes) -> str:
        name = name.lstrip('/')
        self.bucket.put_object(name, data)
        return self.OSS['DOMAIN'] + '/' + name

    def sign_url(self, method, obj_name: str, timeout: int = 60 * 5,
                 file_type='image/jpeg') -> str:
        headers = {
            'Content-Type': file_type
        }
        url = self.bucket.sign_url(
            method, obj_name, timeout, headers=headers)
        return url

    def url(self, obj_name):
        name = obj_name.lstrip('/')
        return self.OSS['DOMAIN'] + '/' + name
