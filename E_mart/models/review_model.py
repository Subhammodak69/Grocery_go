from django.db import models
from E_mart.models import Product,User
from django.core.validators import MinValueValidator , MaxValueValidator

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewed_users')
    review_image = models.URLField(null=True, blank=True)
    review_text = models.TextField(max_length=1000, blank=False, null=False)
    review_stars = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    is_active = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return f"ID:{self.id},reviewed_by:{self.user}, is_active:{self.is_active}"