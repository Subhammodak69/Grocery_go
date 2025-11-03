from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        (1, 'ADMIN'),
        (2, 'ENDUSER'),
        (3, 'DELIVERYWORKER')
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    optional_address = models.TextField(blank=True, null=True)
    role = models.IntegerField(choices=ROLES, default=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
