from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Product
from .serializers import ProductSerializer
from clients.views import BusinessBoundMixin

class ProductViewSet(BusinessBoundMixin, viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(business=self.get_user_business())

    def get_queryset(self):
        business = self.get_user_business()
        return Product.objects.select_related("business").filter(business=business)

    @action(detail=False, methods=["get"])
    def archive(self, request):
        business = self.get_user_business()
        products = Product.deleted_objects.select_related("business").filter(business=business)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        business = self.get_user_business()
        try:
            product = Product.all_objects.get(pk=pk, business=business)

            if not product.deleted:
                return Response(
                    {"error": "Product not in archive."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            product.undelete()
            serializer = self.get_serializer(product)
            return Response(serializer.data)

        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )
