from django.db import models
from E_mart.models import User,Product
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('DELIVERING', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User,related_name= 'orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    listing_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    delivery_address = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'orders'
        
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        db_table = 'orderitems'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
