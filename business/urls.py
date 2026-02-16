from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BusinessViewSet


router = DefaultRouter()
router.register('business', BusinessViewSet, basename='business')

urlpatterns = [
    path('', include(router.urls)),
]