from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment, MpesaTransaction, Escrow, Subscription
from .serializers import PaymentSerializer, EscrowSerializer, SubscriptionSerializer
import requests
from datetime import datetime, timedelta

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def initiate_mpesa(self, request):
        """Initiate M-Pesa STK Push"""
        amount = request.data.get('amount')
        phone_number = request.data.get('phone_number')
        
        if not amount or not phone_number:
            return Response({'error': 'amount and phone_number are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # TODO: Implement M-Pesa integration
        payment = Payment.objects.create(
            user=request.user,
            amount=amount,
            payment_method='mpesa',
            status='pending',
            reference_id=f"MPESA-{datetime.now().timestamp()}",
            description='M-Pesa payment'
        )
        
        MpesaTransaction.objects.create(
            payment=payment,
            phone_number=phone_number
        )
        
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EscrowViewSet(viewsets.ModelViewSet):
    serializer_class = EscrowSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Escrow.objects.filter(models.Q(seller=user) | models.Q(buyer=user))
    
    @action(detail=True, methods=['post'])
    def release_funds(self, request, pk=None):
        escrow = self.get_object()
        if escrow.seller != request.user:
            return Response({'error': 'Only seller can release funds'}, status=status.HTTP_403_FORBIDDEN)
        
        escrow.status = 'released'
        escrow.released_at = datetime.now()
        escrow.save()
        
        serializer = self.get_serializer(escrow)
        return Response(serializer.data)

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def upgrade(self, request):
        tier = request.data.get('tier')
        if not tier:
            return Response({'error': 'tier is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            defaults={'tier': tier, 'renews_at': datetime.now() + timedelta(days=30)}
        )
        
        if not created:
            subscription.tier = tier
            subscription.renews_at = datetime.now() + timedelta(days=30)
            subscription.save()
        
        serializer = self.get_serializer(subscription)
        return Response(serializer.data)
