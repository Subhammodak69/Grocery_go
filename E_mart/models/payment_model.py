# payments/models.py
from django.db import models
from E_mart.models import Order
from E_mart.constants.default_values import PaymentMethod,PaymentStatus

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.IntegerField(choices=((pm.value,pm.name)for pm in PaymentMethod))
    status = models.IntegerField(choices=((ps.value,ps.name) for ps in PaymentStatus), default=1)
    card_details = models.CharField(max_length=100, null=True, blank=True)
    bank_details = models.CharField(max_length=100, null=True, blank=True)
    upi_id = models.CharField(max_length=20, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'payments'
        
    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.status}"
