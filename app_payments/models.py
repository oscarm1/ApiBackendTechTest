from django.db import models
from django.utils import timezone
from app_customers.models import Customer
from app_loans.models import Loan

class Payment(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    customer_external_id = models.ForeignKey(Customer, to_field='external_id', on_delete=models.CASCADE)
    loan_external_id = models.ForeignKey(Loan, to_field='external_id', on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.PositiveIntegerField(choices=[(1, "completed"), (2, "rejected")])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True) 

    def update_loan_status(self, customer, payment_amount):
        loans = Loan.objects.filter(customer_external_id=customer, status=2)
        for loan in loans:
            if payment_amount >= loan.outstanding:
                loan.status = 4 
                payment_amount -= loan.outstanding
                loan.outstanding = 0
            else:
                loan.update_outstanding(payment_amount) 
                payment_amount = 0
            loan.save()

    def __str__(self):
        return self.external_id
