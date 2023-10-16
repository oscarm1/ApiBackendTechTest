from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Customer
from .serializer import CustomerSerializer
from rest_framework.decorators import action
from .services import create_customer, get_customer_balance

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        create_customer(data)  # Llama a la función de servicio para crear un cliente
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'], url_path='customer/(?P<external_id>[^/.]+)/balance/')
    def get_customer_balance(self, request, external_id):
        customer_balance = get_customer_balance(external_id)  # Llama a la función de servicio para obtener el balance
        return Response(customer_balance, status=status.HTTP_200_OK)
