from django.db import models
from E_mart.models import User,Product
from decimal import Decimal

class Cart(models.Model):
    user = models.OneToOneField(User, related_name='cart', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f"{self.user.username}'s cart"

    def get_list_price(self):
        return sum(
            item.product.original_price * item.quantity for item in self.items.filter(is_active=True)
        )
    def get_total_price(self):
        return sum(
            item.product.price * item.quantity for item in self.items.filter(is_active=True)
        )

    def get_discount_price(self):
        total_discount = sum(
            (item.product.original_price - item.product.price) * item.quantity
            for item in self.items.filter(is_active=True)
        )
        return total_discount


    def get_fee_price(self):
        total = self.get_total_price()
        return Decimal('0') if total >= Decimal('500') else Decimal('20')  # delivery charge corrected to 40

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'cartitems'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
