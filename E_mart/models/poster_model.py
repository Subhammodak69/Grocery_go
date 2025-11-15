from django.db import models
from E_mart.models import Product

class Poster(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)
    image = models.URLField(null= False, blank= False)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'posters'
        
    def __str__(self):
        return f"{self.title} Is_Active: {self.image}"
    