# payments/models.py
from django.db import models
from E_mart.models import Order

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('UPI', 'UPI'),
        ('CARD', 'Card'),
        ('COD', 'Cash on Delivery'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'payments'
        
    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.status}"
