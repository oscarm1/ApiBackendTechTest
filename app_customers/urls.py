from django.urls import path, include
from rest_framework import routers
from app_customers import views

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet)

urlpatterns = [
    path('', include(router.urls))
]
