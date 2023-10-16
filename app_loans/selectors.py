from .models import Loan
from .models import Customer

def calculate_total_debt(customer):
    loans = Loan.objects.filter(customer_external_id=customer, status=2)
    total_debt = sum(loan.outstanding for loan in loans)
    return total_debt

def get_customer_by_external_id(external_id):
    try:
        return Customer.objects.get(external_id=external_id)
    except Customer.DoesNotExist:
        return None
    
        # def update_outstanding(self, amount_paid):
        # payments = Payment.objects.filter(loan_external_id=self)
        # total_paid = sum(payment.total_amount for payment in payments)
        # self.outstanding = max(self.amount - total_paid, 0)  # Calcular y asignar monto pendiente
        # self.save()
