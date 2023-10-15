from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Customer, Loan, Payment
from .serializer import CustomerSerializer, LoanSerializer, PaymentSerializer
from rest_framework.decorators import action
from django.db import transaction
from decimal import Decimal

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['GET'], url_path='customer/(?P<external_id>[^/.]+)/balance/')
    def get_customer_balance(self, request, external_id):
        try:
            customer = Customer.objects.get(external_id=external_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        loans = Loan.objects.filter(customer_external_id=customer, status__in=[1, 2])
        total_debt = sum(loan.outstanding for loan in loans)

        customer_score = Decimal(customer.score)

        available_amount = customer_score - total_debt

        data = {
            "external_id": customer.external_id,
            "score": customer_score,
            "available_amount": available_amount,
            "total_debt": total_debt
        }

        return Response(data, status=status.HTTP_200_OK)

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_external_id = serializer.validated_data.get('customer_external_id')
        amount = Decimal(serializer.validated_data.get('amount'))

        try:
            customer = Customer.objects.get(external_id=customer_external_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        if customer.status == 2:
            return Response({"error": "Customer is inactive"}, status=status.HTTP_400_BAD_REQUEST)

        outstanding = amount  # Establecer outstanding igual al amount

        with transaction.atomic():
            loan = serializer.save(status=2, outstanding=outstanding)

        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)

    def calculate_total_debt(self, customer):
        loans = Loan.objects.filter(customer_external_id=customer, status=2)
        total_debt = sum(loan.outstanding for loan in loans)
        return total_debt
    
    @action(detail=False, methods=['GET'],  url_path='loan/(?P<external_id>[^/.]+)/loans-by-customer/')
    def get_loans_by_customer(self, request, external_id):
        try:
            customer = Customer.objects.get(external_id=external_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        loans = Loan.objects.filter(customer_external_id=customer)

        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = serializer.validated_data.get('customer_external_id')
        total_amount = serializer.validated_data.get('total_amount')
        customer = Customer.objects.get(external_id=customer_id)

        if customer.status == 2:
            return Response({"error": "Customer is inactive"}, status=status.HTTP_400_BAD_REQUEST)

        total_debt = self.calculate_total_debt(customer)

        if total_amount > total_debt:
            return Response({"error": "Payment amount exceeds total debt"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            self.perform_create(serializer)
            self.update_loan_status(customer, total_amount)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def calculate_total_debt(self, customer):
        loans = Loan.objects.filter(customer_external_id=customer, status=2)
        total_debt = sum(loan.outstanding for loan in loans)
        return total_debt
    
    def update_loan_status(self, customer, payment_amount):
        loans = Loan.objects.filter(customer_external_id=customer, status=2)
        for loan in loans:
            if payment_amount >= loan.outstanding:
                loan.status = 4  # Cambiar el estado del préstamo a "paid"
                payment_amount -= loan.outstanding
                loan.outstanding = 0
                loan.save()  # Guardar los cambios en el modelo Loan
            else:
                loan.update_outstanding(payment_amount)  # Actualizar el monto pendiente
                payment_amount = 0
                loan.save()  # Guardar los cambios en el modelo Loan
