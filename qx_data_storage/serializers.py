import time
import base64
from rest_framework import serializers
from qx_base.qx_rest.exceptions import SerializerFieldError
from .oss import AutoOssStorage
from .callbacks import callbacks


class OssImageSerializerMixin():
    """
    If use set_image, need set oss_location.
    image_field: model image field.
    """

    def parse_image(self, validated_data, image_field):
        img = validated_data[image_field]
        file_obj = base64.b64decode(img.encode())
        return file_obj

    def push_image(self, obj_name, file_obj):
        try:
            url = AutoOssStorage().put_bytes(obj_name, file_obj)
        except Exception:
            raise SerializerFieldError("上传失败", 'image')
        return url

    def set_image(self, validated_data, image_field, unique_id):
        file_obj = self.parse_image(validated_data, image_field)

        location = self.oss_location.strip('/')
        obj_name = "{}/{}-{}".format(
            location, int(time.time() * 1000), unique_id)

        url = self.push_image(obj_name, file_obj)
        validated_data[image_field] = url
        return url


class UploadImageSerializer(serializers.Serializer, OssImageSerializerMixin):

    image = serializers.CharField(
        label="上传图片(base64)")
    type = serializers.ChoiceField(
        list(callbacks.keys()))
    callback_params = serializers.JSONField(
        label="回调参数", required=False)

    def create(self, validated_data):
        name = validated_data['type']
        callback_params = validated_data.get('callback_params', {})
        user = self.context['request'].user

        instance = callbacks[name](user=user, callback_params=callback_params)
        status, msg = instance.validate()
        if not status:
            raise SerializerFieldError(msg, 'callback_params')

        file_obj = self.parse_image(validated_data, 'image')

        location = instance.location.strip('/')
        obj_name = "{}/{}-{}".format(
            location, int(time.time() * 1000), user.id)
        url = self.push_image(obj_name, file_obj)

        status, msg = instance.upload_image_callback(url)
        if status:
            return validated_data
        else:
            raise SerializerFieldError(msg, 'image')
