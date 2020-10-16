from django.db import models
from qx_data_storage.oss import BackendOssStorage

# Create your models here.


class ImageStar(models.Model):

    image = models.ImageField(
        verbose_name="图片",
        storage=BackendOssStorage(path="/pytest"),
        null=True, blank=True)
    name = models.CharField(
        verbose_name="名称", max_length=100)

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = verbose_name
