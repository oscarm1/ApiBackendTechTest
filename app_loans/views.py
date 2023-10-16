from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Customer, Loan
from .serializer import LoanSerializer
from rest_framework.decorators import action
from .services import create_loan, get_loans_by_customer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        #create_loan(data)
        loan, error = create_loan(data)

        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'], url_path='loan/(?P<external_id>[^/.]+)/loans-by-customer/')
    def get_loans_by_customer(self, request, external_id):
        loans = get_loans_by_customer(external_id)  # Llama a la función de servicio para obtener los préstamos por cliente
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
