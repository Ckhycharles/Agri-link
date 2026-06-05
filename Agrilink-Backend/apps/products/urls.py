from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductReviewViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'products/(?P<product_id>\d+)/reviews', ProductReviewViewSet, basename='product-review')

urlpatterns = [
    path('', include(router.urls)),
]
