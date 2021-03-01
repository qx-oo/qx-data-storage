from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register('storage', viewsets.StorageViewset,
                basename="storage")

urlpatterns = [
    path('', include(router.urls)),
]
