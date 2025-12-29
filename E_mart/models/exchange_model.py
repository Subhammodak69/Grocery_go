from django.db import models
from E_mart.models import User, Product,OrderItem, Order
from E_mart.constants.default_values import ExchangeOrReturnStatus,ExOrRePurpose

class ExchangeOrReturn(models.Model):
    order = models.ForeignKey(Order, related_name='exchange_requests', on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, related_name='exchange_requests', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='exchange_requests', on_delete=models.CASCADE)
    reason = models.TextField()
    product = models.ForeignKey(Product, related_name='exchange_requested', on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=((es.value,es.name)for es in ExchangeOrReturnStatus), default=1)
    processed_date = models.DateTimeField(null=True, blank=True)
    purpose = models.IntegerField(choices=((eo.value,eo.name)for eo in ExOrRePurpose), default=1)


    class Meta:
        db_table = 'exchange_requests'

    def __str__(self):
        return f"Exchange Request for OrderItem {self.order_item.id} - Status: {self.status}"
