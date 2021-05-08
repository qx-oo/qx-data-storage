import traceback
import time
import base64
import binascii
from rest_framework import serializers
from qx_base.qx_rest.exceptions import SerializerFieldError
from .oss import AutoOssStorage
from .callbacks import callbacks


file_type_map = {
    'png': 'image/png',
    'jpeg': 'image/jpeg',
}


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
            traceback.print_exc()
            raise SerializerFieldError("上传失败", 'image')
        return url

    def set_image(self, validated_data, image_field, unique_id):
        try:
            file_obj = self.parse_image(validated_data, image_field)

        except binascii.Error:
            raise serializers.ValidationError("image parse error")

        location = self.oss_location.strip('/')
        obj_name = "{}/{}-{}".format(
            location, int(time.time() * 1000), unique_id)

        try:
            url = self.push_image(obj_name, file_obj)
        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("push oss fail")
        validated_data[image_field] = url
        return url

    def get_upload_url(self, location, unique_id, file_type):
        ts = hex(int(time.time() * 10000000))[2:]
        obj_name = "upload/{}/{}-{}".format(
            location, ts, unique_id)
        try:
            ins = AutoOssStorage()
            upload_url = ins.sign_url('PUT', obj_name, file_type=file_type)
            url = ins.url(obj_name)
        except Exception:
            traceback.print_exc()
            raise serializers.ValidationError("Get upload url error")
        return upload_url, url


class StorageSerializer(serializers.Serializer, OssImageSerializerMixin):

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
            validated_data['image'] = url
            return validated_data
        else:
            raise SerializerFieldError(msg, 'image')


class UploadUrlSerializer(serializers.Serializer, OssImageSerializerMixin):

    upload_url = serializers.CharField(
        label="上传链接", read_only=True)
    url = serializers.CharField(
        label="访问链接", read_only=True)
    type = serializers.ChoiceField(
        list(callbacks.keys()))
    file_type = serializers.ChoiceField(
        list(file_type_map.keys()))

    def create(self, validated_data):
        name = validated_data['type']
        user = self.context['request'].user
        file_type = validated_data['file_type']
        if not (file_type := file_type_map.get(file_type)):
            raise SerializerFieldError('file type error', 'file_type')

        upload_url, url = self.get_upload_url(name, user.id, file_type)

        validated_data['upload_url'] = upload_url
        validated_data['url'] = url
        return validated_data
