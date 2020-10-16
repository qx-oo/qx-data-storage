from qx_base.settings import get_settings


QX_DATA_STORAGE_SETTINGS = {
    "ALIYUN_OSS": {
        "DOMAIN": "",
        "ENDPOINT": "",
        "BUCKET_NAME": "",
        "ACCESS_KEY_ID": "",
        "ACCESS_KEY_SECRET": "",
    },
}

data_storage_settings = get_settings(
    'QX_DATA_STORAGE_SETTINGS', QX_DATA_STORAGE_SETTINGS)
