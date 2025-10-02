from django.db import models
from E_mart.models import Product

class ProductDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='product_details')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_details'

    def __str__(self):
        return f"ID: {self.id} is_active: {self.is_active} Product: {self.product}"