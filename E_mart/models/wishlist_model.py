from django.db import models
from E_mart.models import Product,User

class Wishlist(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)    

    class Meta:
        db_table = 'wishlists'

    def __str__(self):
        return f"ID:{self.id},created_by: {self.created_by} "