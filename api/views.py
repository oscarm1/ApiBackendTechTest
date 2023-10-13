from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializer import CustomerSerializer, LoanSerializer, PaymentSerializer
from .models import Customer, Loan, Payment
from rest_framework.decorators import action

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True, methods=['get'])
    def get_balance(self, request, pk=None):
        customer = self.get_object()
        total_debt = sum(loan.outstanding for loan in customer.loans.filter(status__in=[1, 2]))
        available_amount = customer.score - total_debt
        response_data = {
            'external_id': customer.external_id,
            'score': customer.score,
            'available_amount': available_amount,
            'total_debt': total_debt,
        }
        return Response(response_data)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(status=1)  # Cliente creado con estado activo
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(status=2)  # Préstamo creado con estado activo
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        customer_external_id = request.query_params.get('customer_external_id')
        if customer_external_id:
            queryset = queryset.filter(customer__external_id=customer_external_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Verificar si el pago es mayor que la deuda total del préstamo
        loan = serializer.validated_data['loan']
        total_outstanding = loan.outstanding
        total_payment = serializer.validated_data['total_amount']

        if total_payment > total_outstanding:
            return Response({'error': 'El pago excede la deuda del préstamo.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)