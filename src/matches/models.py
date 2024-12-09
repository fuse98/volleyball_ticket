from django.db import models
from users.models import CustomUser


class Stadium(models.Model):
    title = models.CharField(max_length=100)
    address = models.TextField()
    lat = models.FloatField()
    long = models.FloatField()

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
