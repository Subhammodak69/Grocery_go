from django.contrib.auth.models import AbstractUser
from django.db import models
from E_mart.constants.default_values import Role

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    optional_address = models.TextField(blank=True, null=True)
    role = models.IntegerField(choices=((r.value,r.name) for r in Role), default=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
