from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(business=self.request.user.business)

    def get_queryset(self):
        return Product.objects.select_related(
            "business"
            ).filter(
                business=self.request.user.business
                )

    @action(detail=False, methods=["get"])
    def archive(self, request):
        products = Product.deleted_objects.select_related(
            "business"
            ).filter(
                business=self.request.user.business
                )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        try:
            product = Product.all_objects.get(pk=pk, business=self.request.user.business)

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