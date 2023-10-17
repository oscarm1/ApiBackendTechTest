from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='Api OM Documentation')),
    path('api/v1/customer/', include('app_customers.urls')),  
    path('api/v1/loan/', include('app_loans.urls')), 
    path('api/v1/payment/', include('app_payments.urls')),
]
