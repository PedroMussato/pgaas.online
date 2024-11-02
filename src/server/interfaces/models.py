from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DataBaseInstace(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)