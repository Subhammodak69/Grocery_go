from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField( max_length=150, blank=True)
    last_name = models.CharField( max_length=150, blank=True)
    email = models.EmailField(unique=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'users'
        
    def __str__(self):
        return self.username
