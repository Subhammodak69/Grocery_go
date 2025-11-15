from django.db import models
from E_mart.models import User,OrderItem
from E_mart.constants.default_values import HelpStatus

class Help(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problem_histories')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='problem_items')
    problem = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=((hs.value,hs.name) for hs in HelpStatus), default=1)
    def __str__(self):
        return f"Problem for {self.user.username} ({self.status})"
