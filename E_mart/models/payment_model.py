# payments/models.py
from django.db import models
from E_mart.models import Order

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('UPI', 'UPI'),
        ('CREDIT_CARD', 'CreditCard'),
        ('DEBIT_CARD', 'DebitCard'),
        ('NETBANKING', 'Netbanking'),
        ('COD', 'Cash on Delivery'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
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
