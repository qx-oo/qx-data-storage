# qx-data-storage
my django project data storage module

### Install:

    $ pip install -e git://github.com/qx-oo/qx-data-storage.git@master#egg=qx-data-storage

### Usage:

settings.py:

    INSTALLED_APPS = [
        ...
        'qx_data_storage',
        ...
    ]


    QX_DATA_STORAGE_SETTINGS = {
        "ALIYUN_OSS": {
            "DOMAIN": "https://oss.xxx.com.cn",
            "ENDPOINT": "oss-cn-shanghai.aliyuncs.com",
            "BUCKET_NAME": "xxx",
            "ACCESS_KEY_ID": ALIYUN_ACCESS_KEY_ID,
            "ACCESS_KEY_SECRET": ALIYUN_ACCESS_KEY_SECRET,
        },
    }

models.py:

    from qx_data_storage.oss import BackendOssStorage

    class ImageModel(models.Model):

        ...
        image = models.ImageField(
            verbose_name="Image",
            storage=BackendOssStorage(path="/pytest"),
            null=True, blank=True)
        
        ...

Upload Image Model:

    @register_upload_callback
    class UploadImageStar(UploadModelImageCallbackMixin):
        model = ImageStar
        image_field = 'image'
        name = 'star_image'

urls.py:

    urlpatterns = [
        ...
        path('upload/', include('qx_data_storage.urls')),
        ...
    ]