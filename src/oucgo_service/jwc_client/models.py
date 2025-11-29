# jwc_client/models.py
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    jwc_username = models.CharField(max_length=64)
    jwc_password = models.CharField(max_length=128)
    last_fetch = models.DateTimeField(null=True, blank=True)
    last_html_hash = models.CharField(max_length=64, null=True, blank=True)
    
    def __str__(self):
        return self.user.username