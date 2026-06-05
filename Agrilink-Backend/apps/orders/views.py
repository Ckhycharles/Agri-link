from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem, Delivery, Rating
from .serializers import OrderSerializer, RatingSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(models.Q(buyer=user) | models.Q(seller=user))
    
    @action(detail=False, methods=['get'])
    def my_purchases(self, request):
        orders = Order.objects.filter(buyer=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_sales(self, request):
        orders = Order.objects.filter(seller=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        if order.seller != request.user:
            return Response({'error': 'Only seller can confirm order'}, status=status.HTTP_403_FORBIDDEN)
        
        order.status = 'confirmed'
        order.save()
        return Response(self.get_serializer(order).data)
    
    @action(detail=True, methods=['post'])
    def ship(self, request, pk=None):
        order = self.get_object()
        if order.seller != request.user:
            return Response({'error': 'Only seller can ship order'}, status=status.HTTP_403_FORBIDDEN)
        
        order.status = 'shipped'
        order.save()
        
        # Create delivery record if not exists
        if not hasattr(order, 'delivery'):
            Delivery.objects.create(
                order=order,
                recipient_address=request.data.get('address', ''),
                recipient_phone=request.data.get('phone', '')
            )
        
        return Response(self.get_serializer(order).data)
    
    @action(detail=True, methods=['post'])
    def deliver(self, request, pk=None):
        order = self.get_object()
        order.status = 'delivered'
        order.save()
        
        if hasattr(order, 'delivery'):
            delivery = order.delivery
            delivery.status = 'delivered'
            delivery.save()
        
        return Response(self.get_serializer(order).data)
    
    @action(detail=True, methods=['post'])
    def add_rating(self, request, pk=None):
        order = self.get_object()
        
        if order.buyer != request.user and order.seller != request.user:
            return Response({'error': 'Only order participants can rate'}, status=status.HTTP_403_FORBIDDEN)
        
        rating, created = Rating.objects.get_or_create(order=order)
        
        if order.buyer == request.user:
            rating.buyer_rating = request.data.get('rating')
            rating.buyer_comment = request.data.get('comment', '')
        else:
            rating.seller_rating = request.data.get('rating')
            rating.seller_comment = request.data.get('comment', '')
        
        rating.save()
        return Response(RatingSerializer(rating).data)
