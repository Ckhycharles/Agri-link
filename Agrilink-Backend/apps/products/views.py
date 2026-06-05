from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Product, ProductReview, ProductImage
from .serializers import ProductSerializer, ProductReviewSerializer, ProductImageSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Product.objects.all()
        return Product.objects.filter(status='active')
    
    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)
    
    def perform_update(self, serializer):
        if serializer.instance.farmer != self.request.user:
            raise PermissionError("You can only edit your own products")
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def my_products(self, request):
        products = Product.objects.filter(farmer=request.user)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_image(self, request, pk=None):
        product = self.get_object()
        image = request.FILES.get('image')
        if image:
            ProductImage.objects.create(product=product, image=image)
            return Response({'status': 'image added'})
        return Response({'error': 'image is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def nearby(self, request, pk=None):
        """Get nearby products based on farmer location"""
        product = self.get_object()
        nearby = Product.objects.filter(
            status='active',
            farmer__farm__latitude__range=(
                product.farmer.farm.latitude - 0.1,
                product.farmer.farm.latitude + 0.1
            ),
            farmer__farm__longitude__range=(
                product.farmer.farm.longitude - 0.1,
                product.farmer.farm.longitude + 0.1
            )
        ).exclude(id=pk)[:10]
        serializer = self.get_serializer(nearby, many=True)
        return Response(serializer.data)

class ProductReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductReview.objects.filter(product_id=product_id)
    
    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        serializer.save(product_id=product_id, reviewer=self.request.user)
