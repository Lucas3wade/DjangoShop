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
    products = models.ManyToManyField("Product", through="OrderedProducts")

    def get_total_price(self):
        total = 0
        ordered_products = OrderedProducts.objects.filter(order=self)
        for ordered_product in ordered_products:
            total+=ordered_product.amount * ordered_product.product.price
        return total

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class OrderedProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

