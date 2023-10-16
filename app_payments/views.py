from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Customer, Loan, Payment
from .serializer import PaymentSerializer
from .services import create_payment

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        payment, error = create_payment(data)  # Llama a la función de servicio para crear un pago

        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
