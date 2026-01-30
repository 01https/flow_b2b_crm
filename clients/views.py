from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=False, methods=["get"])
    def archive(self, request):
        archived_clients = Client.deleted_objects.all()
        serializer = self.get_serializer(archived_clients, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        try:
            client = Client.all_objects.get(pk=pk)
            
            if not client.deleted:  # перевірка (опціонально)
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