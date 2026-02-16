from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from .serializers import BusinessSerializer
from .models import Business
from .permissions import IsOwner

class BusinessViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
    ):
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Business.objects.select_related(
            "owner"
            ).filter(
                owner=self.request.user
                )
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)