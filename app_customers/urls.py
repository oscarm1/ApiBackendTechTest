from django.urls import path, include
from rest_framework import routers
from app_customers import views

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
# router.register(r'loans', views.LoanViewSet)
# router.register(r'payments', views.PaymentViewSet)

urlpatterns = [
    path('', include(router.urls))
]
