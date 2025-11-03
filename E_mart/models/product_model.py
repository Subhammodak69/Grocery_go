from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    image = models.URLField(blank=False, null=False)

    class Meta:
        db_table = 'categories'
        
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    size = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    image = models.URLField()

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name
