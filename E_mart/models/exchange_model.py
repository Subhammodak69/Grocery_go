from django.db import models
from E_mart.models import User, Product,OrderItem, Order

class ExchangeRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('EXCHANGED', 'Exchanged'),
    ]

    order = models.ForeignKey(Order, related_name='exchange_requests', on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, related_name='exchange_requests', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='exchange_requests', on_delete=models.CASCADE)
    reason = models.TextField()
    requested_product = models.ForeignKey(Product, related_name='exchange_requested', on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    processed_date = models.DateTimeField(null=True, blank=True)
    admin_note = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'exchange_requests'

    def __str__(self):
        return f"Exchange Request for OrderItem {self.order_item.id} - Status: {self.status}"
