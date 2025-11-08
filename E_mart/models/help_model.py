from django.db import models
from E_mart.models import User,OrderItem

class ProblemHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problem_histories')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='problem_items')
    problem_description = models.TextField()
    resolution = models.TextField(blank=True, null=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_problems')
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Problem for {self.user.username} ({self.status})"
