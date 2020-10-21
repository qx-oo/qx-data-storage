from django.db import models
from django.conf import settings
from qx_data_storage.oss import BackendOssStorage
from qx_data_storage.callbacks import (
    register_upload_callback, UploadModelImageCallbackMixin
)

# Create your models here.


class ImageStar(models.Model):

    image = models.ImageField(
        verbose_name="图片",
        storage=BackendOssStorage(path="/pytest"),
        null=True, blank=True)
    name = models.CharField(
        verbose_name="名称", max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = verbose_name


@register_upload_callback
class UploadImageStar(UploadModelImageCallbackMixin):
    model = ImageStar
    image_field = 'image'
    name = 'star_image'
