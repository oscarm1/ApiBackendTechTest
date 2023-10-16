from .models import Customer, Loan

def calculate_total_debt(customer):
    loans = Loan.objects.filter(customer_external_id=customer, status=2)
    total_debt = sum(loan.outstanding for loan in loans)
    return total_debt

def get_customer_by_external_id(external_id):
    try:
        return Customer.objects.get(external_id=external_id)
    except Customer.DoesNotExist:
        return None

def get_loan_by_external_id(external_id):
    try:
        return Loan.objects.get(external_id=external_id)
    except Loan.DoesNotExist:
        return None
