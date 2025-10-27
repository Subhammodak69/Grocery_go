from django.db import models
from E_mart.models import Product

class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers')
    percentage = models.IntegerField(blank=False,null=False)
    starts_at = models.DateTimeField(blank=False,null=False)
    ends_at = models.DateTimeField(blank=False,null=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'offers'

    def __str__(self):
        return f"ID:{self.id}, product_id:{self.product.id}"