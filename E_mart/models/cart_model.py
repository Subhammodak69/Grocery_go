from django.db import models
from E_mart.models import User,productdetails_model

class Cart(models.Model):
    user = models.OneToOneField(User,related_name= 'cart', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"{self.user.username}'s cart"
    
    def get_total_price(self):
        # Correctly reference product price and quantity from each item
        return sum(
            item.product_details.price * item.quantity for item in self.items.filter(is_active = True)
        )

    def get_discount_price(self):
        total = self.get_total_price()
        # Example: 10% discount for orders above 1000 rupees
        if total >= 2000:
            return total * 0.30
        elif total >= 1000:
            return total * 0.20
        elif total >= 500:
            return total * 0.10
        return 0

    def get_fee_price(self):
        total = self.get_total_price()
        # Example: Free delivery above 500; else, ₹40 delivery charge
        return 0 if total >= 500 else 20

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    product_details = models.ForeignKey(productdetails_model.ProductDetails, on_delete=models.CASCADE, related_name='items')
    class Meta:
        db_table = 'cartitems'
        
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
