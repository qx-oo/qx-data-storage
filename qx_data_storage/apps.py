from django.apps import AppConfig, apps
from .callbacks import uploadurl_map, UploadUrlMixin


class QxDataStorageConfig(AppConfig):
    name = 'qx_data_storage'

    def ready(self) -> None:
        for app in apps.get_models():
            if issubclass(app, UploadUrlMixin):
                uploadurl_map[app._upload_name] = app
