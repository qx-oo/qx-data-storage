from .mixins import UploadImageCallbackMixin, UploadUrlMixin


callbacks = {}

uploadurl_map = {}


def register_upload_callback(cls):
    """
    Upload Image Callback
    example:
        @register_upload_callback
        class TestCallback(UploadImageCallbackMixin):
            name = "test1"

            def validate(self):
                if self.user:
                    return True, ''
                return False, 'user error'

            def upload_image_callback(self, url):
                return True
    """
    if issubclass(cls, UploadImageCallbackMixin):
        if isinstance(cls.name, str):
            callbacks[cls.name] = cls
        else:
            raise Exception("{} name error".format(cls.__name__))
    else:
        raise Exception(
            "{} need extend UploadImageCallbackMixin".format(cls.__name__))


def register_upload_url_callback(cls):
    if issubclass(cls, UploadUrlMixin):
        uploadurl_map[cls._upload_name] = cls
    else:
        raise Exception(
            "{} need extend UploadImageCallbackMixin".format(cls.__name__))
