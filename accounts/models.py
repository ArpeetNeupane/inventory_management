from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True) #unique phone number, optional in forms and can be null for people with no number

    def __str__(self):
        return self.username
