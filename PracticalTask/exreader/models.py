from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')