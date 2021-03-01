import typing
from django.db.models.fields.files import FileDescriptor


callbacks = {}


class UploadImageCallbackMixin():

    def __init__(self, user, callback_params=dict):
        self.user = user
        self.callback_params = callback_params

    @property
    def name(self):
        raise NotImplementedError

    location = "upload/image"

    def validate(self) -> typing.Tuple[bool, str]:
        """
        validate params
        return: status, error msg
        """
        raise NotImplementedError

    def upload_image_callback(self, url) -> typing.Tuple[bool, str]:
        """
        Upload Image Callback
        return: status, error msg
        """
        raise NotImplementedError


class UploadModelImageCallbackMixin(UploadImageCallbackMixin):
    """
    model, image_field, object_field, user_field required
    """

    @property
    def location(self):
        location = getattr(self.model, self.image_field).field.storage.location
        return location

    @property
    def model(self):
        raise NotImplementedError

    @property
    def image_field(self):
        raise NotImplementedError

    user_field = 'user'

    object_field = 'id'

    def validate(self) -> typing.Tuple[bool, str]:
        """
        validate params
        return: status, error msg
        """
        object_id = self.callback_params.get('object_id')

        image = getattr(self.model, self.image_field, None)
        if not isinstance(image, FileDescriptor):
            return False, "image_field error"
        if object_id is None:
            return False, "object_id required"
        query = {
            self.object_field: object_id,
            self.user_field: self.user.id
        }
        try:
            self.instance = self.model.objects.get(**query)
        except Exception:
            return False, "instance lookup fail"
        return True, ''

    def upload_image_callback(self, url) -> typing.Tuple[bool, str]:
        try:
            setattr(self.instance, self.image_field, url)
            self.instance.save()
        except Exception:
            return False, "save error"
        return True, ''


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
