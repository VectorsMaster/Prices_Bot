from django.db import models

# Create your models here.

class Product(models.Model):
    id  = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    price_sp = models.DecimalField(max_digits=10, decimal_places=1)
    name_arabic = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=1028, blank=True, null=True)
    vehicle_type = models.CharField(max_length=128, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
