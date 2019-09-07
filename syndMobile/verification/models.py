from django.db import models

class RegisteredNo(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    phone = models.CharField(max_length=10)
    name = models.CharField(max_length=30, blank=True)