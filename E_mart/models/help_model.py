from django.db import models
from E_mart.models import User, OrderItem
from E_mart.constants.default_values import HelpStatus

class Help(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problem_histories')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='problem_items')
    problem = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=((hs.value,hs.name) for hs in HelpStatus), default=1)
    is_active = models.BooleanField(default=True)
    
    # New fields for better tracking
    admin_response = models.TextField(blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(default=1, choices=[(1,'Low'),(2,'Medium'),(3,'High')])
    
    class Meta:
        db_table = "helps"
        ordering = ['-reported_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['user', 'status']),
        ]

    
    def __str__(self):
        return f"Problem for {self.user.username} ({self.get_status_display()})"
    
    def mark_as_resolved(self):
        from django.utils import timezone
        self.status = 3  # Assuming 3 is Resolved
        self.resolved_at = timezone.now()
        self.save()


class ContactMessage(models.Model):
    SUBJECT_CHOICES = (
        ('order', 'Order Issue'),
        ('product', 'Product Question'),
        ('delivery', 'Delivery Problem'),
        ('payment', 'Payment Issue'),
        ('feedback', 'Feedback'),
        ('other', 'Other'),
    )
    
    STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'In Progress'),
        (3, 'Resolved'),
        (4, 'Closed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject_type = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    admin_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        db_table = "contact_messages"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.name}"


class FAQ(models.Model):
    CATEGORY_CHOICES = (
        ('order', 'Orders'),
        ('delivery', 'Delivery'),
        ('payment', 'Payments'),
        ('returns', 'Returns & Refunds'),
        ('account', 'Account'),
        ('general', 'General'),
    )
    
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "faqs"
        ordering = ['category', 'order']
    
    def __str__(self):
        return self.question


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100)
    message = models.TextField()
    is_bot = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "chat_messages"
        ordering = ['created_at']