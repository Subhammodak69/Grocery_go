# delivery/models.py
from django.db import models
from E_mart.models import User,Order
from E_mart.constants.default_values import DeliveryStatus

class DeliveryPerson(models.Model):
    user = models.OneToOneField(User, related_name='deliveries', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    amount = models.IntegerField(blank=True, null=True)
    
    class Meta:
        db_table = 'deliverypersons'
        
    def __str__(self):
        return self.user.username

class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.TextField(blank=False, null=False)
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(choices=((ds.value,ds.name) for ds in DeliveryStatus), default= 1)
    assigned_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'deliveries'

    def __str__(self):
        return f"Delivery for Order {self.order.id} - {self.status}"
