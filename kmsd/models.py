from django.contrib.auth.models import User
from django.db import models


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    _class = models.CharField(max_length=255)
