from django.db import models
from django.contrib.auth.models import User
import uuid 

# Create your models here.
class DataBaseInstace(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    instance_cpu = models.FloatField(default=0.1)
    instance_ram = models.IntegerField(default=128)
    instance_disk = models.IntegerField(default=100)
    status = models.CharField(max_length=256, default='on-creation')
    password = models.CharField(max_length=256, default='')
    port = models.IntegerField(default=0)

class AgentToken(models.Model):
    name = models.CharField(max_length=256, default='')
    uuid = models.UUIDField(default = uuid.uuid4)
