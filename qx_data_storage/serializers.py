import time
from rest_framework import serializers
from qx_base.qx_rest.exceptions import SerializerFieldError
from .oss import AutoOssStorage
from .callbacks import callbacks


class UploadImageSerializer(serializers.Serializer):

    image = serializers.ImageField(
        label="上传图片")
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

        file_obj = validated_data['image']

        location = instance.location.rstrip('/')
        obj_name = "{}/{}-{}".format(
            location, int(time.time() * 1000), user.id)
        try:
            url = AutoOssStorage().put_bytes(obj_name, file_obj)
        except Exception:
            raise SerializerFieldError("上传失败", 'image')

        status, msg = instance.upload_image_callback(url)
        if status:
            return validated_data
        else:
            raise SerializerFieldError(msg, 'image')
