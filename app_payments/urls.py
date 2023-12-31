from django.urls import path, include
from rest_framework import routers
from app_payments import views

router = routers.DefaultRouter()
router.register(r'payments', views.PaymentViewSet)

urlpatterns = [
    path('', include(router.urls))
]
