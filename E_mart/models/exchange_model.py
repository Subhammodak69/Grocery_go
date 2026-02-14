from django.db import models
from E_mart.models import User, OrderItem, Order
from E_mart.constants.default_values import ExchangeOrReturnStatus, ExOrRePurpose


class ExchangeOrReturn(models.Model):
    order = models.ForeignKey(Order, related_name='exchange_requests', on_delete=models.CASCADE) 
    user = models.ForeignKey(User, related_name='exchange_requests', on_delete=models.CASCADE)
    reason = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=[(es.value, es.name) for es in ExchangeOrReturnStatus], default=1) 
    processed_date = models.DateTimeField(null=True, blank=True)
    purpose = models.IntegerField(choices=[(eo.value, eo.name) for eo in ExOrRePurpose], default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'exchange_requests'

    def __str__(self):
        return f"ID: {self.id} - Status: {self.status}"


class ExOrReItems(models.Model):
    exchange_or_return = models.ForeignKey(ExchangeOrReturn, on_delete=models.CASCADE, related_name='exchange_return_items')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='exchange_return_items') 
    quantity = models.PositiveIntegerField(default=1)  
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'exchange_or_return_items' 

    def __str__(self):
        return f"ID: {self.id} - Active: {self.is_active}"
