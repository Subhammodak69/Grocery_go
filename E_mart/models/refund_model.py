from django.db import models
from E_mart.models import Order,OrderItem,User

class RefundRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('PROCESSED', 'Processed'),
    ]

    order = models.ForeignKey(Order, related_name='refund_requests', on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, related_name='refund_requests', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='refund_requests', on_delete=models.CASCADE)
    reason = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    processed_date = models.DateTimeField(null=True, blank=True)
    admin_note = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'refund_requests'

    def __str__(self):
        return f"Refund Request for OrderItem {self.order_item.id} - Status: {self.status}"

