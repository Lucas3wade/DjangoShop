from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    description = models.CharField(default='brak opisu', max_length=500)
    weight = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    shipping_method = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + ' ' + self.last_name