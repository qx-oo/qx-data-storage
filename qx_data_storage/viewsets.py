from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.decorators import action
from qx_base.qx_rest.response import ApiResponse
from .serializers import StorageSerializer, UploadUrlSerializer


class StorageViewset(viewsets.GenericViewSet,):
    """
    Object Storage
    ---
    create:
        Upload Object

        Upload Object

    upload_url:
        Get Upload url

        Get Upload url
    """

    permission_classes = (
        IsAuthenticated,
    )

    serializer_class = StorageSerializer

    def get_serializer_class(self):
        if self.action == 'upload_url':
            return UploadUrlSerializer
        return StorageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ret = serializer.save()
        return ApiResponse(data=ret)

    @action(methods=['post'], url_path='upload-url', detail=False)
    def upload_url(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ret = serializer.save()
        return ApiResponse(data=ret)
