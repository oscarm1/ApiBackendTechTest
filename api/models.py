from django.db import models

"""class Programmer(models.Model):
    fullname = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)"""

class Customer(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    score = models.FloatField()
    status = models.PositiveIntegerField(choices=[(1, "Activo"), (2, "Inactivo")], default=1)

    def __str__(self):
        return self.external_id
    

class Loan(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField()
    contract_version = models.CharField(max_length=100, blank=True, null=True)
    status = models.PositiveIntegerField(choices=[
        (1, "pending"),
        (2, "active"),
        (3, "rejected"),
        (4, "paid")
    ], default=1)
    outstanding = models.FloatField()

    def __str__(self):
        return self.external_id


class Payment(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    status = models.PositiveIntegerField(choices=[(1, "completed"), (2, "rejected")])

    def __str__(self):
        return self.external_id
