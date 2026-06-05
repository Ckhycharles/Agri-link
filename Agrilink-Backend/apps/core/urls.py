from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FarmViewSet, SubscriptionViewSet
from .auth_views import AuthViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'farms', FarmViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
