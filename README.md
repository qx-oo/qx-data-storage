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
            "ACCESS_KEY_ID": "xxx",
            "ACCESS_KEY_SECRET": "xxx",
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
