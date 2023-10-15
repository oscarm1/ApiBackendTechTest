from django.db import models
from django.utils import timezone

class Customer(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    status = models.PositiveIntegerField(choices=[(1, "Activo"), (2, "Inactivo")], default=1)
    score = models.FloatField()
    preapproved_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.external_id

class Loan(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    customer_external_id = models.ForeignKey(Customer, to_field='external_id', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    outstanding = models.DecimalField(max_digits=10, decimal_places=2)  # Nuevo campo para monto pendiente
    # @property
    # def outstanding(self):
    #     payments = Payment.objects.filter(loan_external_id=self)
    #     total_paid = sum(payment.total_amount for payment in payments)
    #     return self.amount - total_paid
    status = models.PositiveIntegerField(choices=[
        (1, "pending"),
        (2, "active"),
        (3, "rejected"),
        (4, "paid")
    ], default=1)
    contract_version = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    maximun_payment_date = models.DateTimeField(null=True)
    taken_at = models.DateTimeField(null=True)

    def update_outstanding(self, amount_paid):
        payments = Payment.objects.filter(loan_external_id=self)
        total_paid = sum(payment.total_amount for payment in payments)
        self.outstanding = max(self.amount - total_paid, 0)  # Calcular y asignar monto pendiente
        self.save()

    def __str__(self):
        return self.external_id

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
