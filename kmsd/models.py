from django.contrib.auth.models import User
from django.db import models


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    grade = models.CharField(max_length=255)


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    grade = models.CharField(max_length=255)


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    present_days = models.IntegerField(default=0)
    grade = models.IntegerField(default=0)