from django.db import models
from django.db.models import Model
from django.utils import timezone
from django.urls import reverse



# Create your models here.

class Class(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Computer(models.Model):
    name = models.CharField(max_length=20)
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='computers')
    def __str__(self):
        return self.name

class User(Model):
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    last_reported = models.DateTimeField(default=timezone.now)
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE, related_name='users')
    def __str__(self):
        return f'{self.first_name} {self.last_name}'



