from decimal import Decimal
from .models import Customer
from app_loans.models import Loan
from .selectors import get_customer_by_external_id
from django.utils import timezone

def create_customer(data):
    customer = Customer.objects.create(
         external_id=data['external_id'],
        status=data.get('status', 1),  # Activo por defecto si no se proporciona
        score=data['score'],
        preapproved_at=timezone.now()  # Establecer preapproved_at en la fecha y hora actual
    )

def get_customer_balance(external_id):
    customer = get_customer_by_external_id(external_id)

    if not customer:
        return {"error": "Customer not found"}, None

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

    return data, None
