import logging
import os
import six
import oss2
from urllib import parse
from django.utils.encoding import force_text
from .django_oss_storage.backends import OssStorage
from .settings import data_storage_settings

logger = logging.getLogger(__name__)


OSS = data_storage_settings.ALIYUN_OSS


class BackendOssStorage(OssStorage):

    def __init__(self, access_key_id=OSS.get('ACCESS_KEY_ID'),
                 access_key_secret=OSS.get('ACCESS_KEY_SECRET'),
                 end_point=OSS.get('ENDPOINT'),
                 bucket_name=OSS.get('BUCKET_NAME'),
                 path="/backend"):
        self.location = path

        super().__init__(
            access_key_id, access_key_secret, end_point, bucket_name)

    def url(self, name, expire=24 * 60 * 60):
        if not name or name.startswith("http"):
            return name
        key = self._get_key_name(name)
        return parse.urljoin(OSS['DOMAIN'], key)

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
        base_path = force_text(self.location)
        if name.startswith(base_path):
            return name
        final_path = parse.urljoin(base_path + "/", name)
        name = os.path.normpath(final_path.lstrip('/'))

        if six.PY2:
            name = name.encode('utf-8')
        return name


class AutoOssStorage():

    def __init__(self, appid=OSS.get('ACCESS_KEY_ID'),
                 appsecret=OSS.get('ACCESS_KEY_SECRET'),
                 bucket_name=OSS.get('BUCKET_NAME')):
        auth = oss2.Auth(appid, appsecret)
        self.bucket = oss2.Bucket(
            auth, 'https://{}'.format(OSS.get('ENDPOINT')),
            bucket_name)

    def put_bytes(self, name: str, data: bytes) -> str:
        self.bucket.put_object(name, data)
        return OSS['DOMAIN'] + '/' + name

    def sign_url(self, obj_name: str, timeout: int = 60) -> str:
        url = self.bucket.sign_url('GET', '<yourObjectName>', timeout)
        return {
            'url': url
        }
