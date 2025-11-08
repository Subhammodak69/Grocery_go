from django.db import models
from E_mart.models import User,Product
from E_mart.constants.default_values import OrderStatus

class Order(models.Model):
    user = models.ForeignKey(User,related_name= 'orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=((o.value,o.name)for o in OrderStatus), default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    listing_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    delivery_address = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    items = models.ManyToManyField(Product, through='OrderItem')
    
    class Meta:
        db_table = 'orders'
        
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'orderitems'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
