# purchases/models.py

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Supplier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.supplier_name


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="purchases"
    )
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        self.total_amount = self.calculated_total_amount
        self.due_amount = self.calculated_due_amount

        super().save(*args, **kwargs)
