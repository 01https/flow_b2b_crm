from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from .models import Client, Note
from .serializers import ClientReadSerializer, ClientDetailSerializer, NoteSerializer


class BusinessBoundMixin:
    def get_user_business(self, user=None):
        user = user or self.request.user
        try:
            return user.owned_business
        except ObjectDoesNotExist:
            raise ValidationError({"business": "Create a business first."})


class ClientViewSet(BusinessBoundMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        business = self.get_user_business(self.request.user)
        return Client.objects.filter(
            business=business
        ).select_related("business").prefetch_related("products")

    def perform_create(self, serializer):
        serializer.save(business=self.get_user_business(self.request.user))

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClientReadSerializer
        return ClientDetailSerializer

    @action(detail=False, methods=["get"])
    def archive(self, request):
        business = self.get_user_business(request.user)
        archived_clients = Client.deleted_objects.filter(business=business)
        serializer = self.get_serializer(archived_clients, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        business = self.get_user_business(request.user)
        try:
            client = Client.all_objects.get(pk=pk, business=business)

            if not client.deleted:
                return Response(
                    {"error": "Client not in archive"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            client.undelete()
            serializer = self.get_serializer(client)
            return Response(serializer.data)

        except Client.DoesNotExist:
            return Response(
                {"error": "Client not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class NoteViewSet(BusinessBoundMixin, viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        business = self.get_user_business(self.request.user)
        queryset = Note.objects.select_related("client").filter(client__business=business)
        client_id = self.request.query_params.get("client")
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        return queryset.order_by("-id")
    
    def perform_create(self, serializer):
        business = self.get_user_business(self.request.user)
        client_id = self.request.query_params.get("client")
        if not client_id:
            raise ValidationError({"client": "client query param is required"})
        
        client = get_object_or_404(Client, pk=client_id, business=business)
        
        serializer.save(client=client)
