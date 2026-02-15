from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import Client
from .serializers import ClientReadSerializer, ClientDetailSerializer


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_user_business(user):
        if hasattr(user, 'owned_business'):
            return user.owned_business
        return user.business

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