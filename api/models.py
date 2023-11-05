from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ShortURL(models.Model):
    
    STATE_CHOICES = [
        ('EXP', 'EXPIRED'),
        ('ACT', 'ACTIVE')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.URLField()
    short_code = models.CharField(max_length=7, unique=True)
    expiry_time = models.DateField()
    uses_left = models.PositiveIntegerField(default = 10)
    status = models.TextField( choices=STATE_CHOICES, default='ACT')

    class Meta:
        indexes = [
            models.Index(fields=['short_code'])
        ]

class URLUsageLog(models.Model):
    short_url = models.ForeignKey(ShortURL, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    access_time = models.DateTimeField(auto_now_add=True)
    

