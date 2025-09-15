from django.db import models
from E_mart.models import User,Product

class Cart(models.Model):
    user = models.OneToOneField(User,related_name= 'cart', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"{self.user.username}'s cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'cartitems'
        
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
