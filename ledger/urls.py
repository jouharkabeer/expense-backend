from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TransactionViewSet, summary


router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', summary, name='summary'),
]


