from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated,
)
from qx_base.qx_rest.response import ApiResponse
from .serializers import UploadImageSerializer


class UploadImageViewset(viewsets.GenericViewSet,):
    """
    Upload Image
    ---
    create:
        Upload Image

        Upload Image
    """

    permission_classes = (
        IsAuthenticated,
    )

    filterset_class = UploadImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse(data=request.data)
