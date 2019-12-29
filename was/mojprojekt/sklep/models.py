from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from statistics import mean


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    description = models.CharField(default='brak opisu', max_length=500)
    weight = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def get_all_opinions(self):
        all_opinions = Opinion.objects.filter(product=self)
        return all_opinions

    def get_grade(self):
        grades = []
        all_opinions = Opinion.objects.filter(product=self)
        for opinion in all_opinions:
            grades.append(opinion.grade)
        if len(all_opinions) > 0:
            return mean(grades)
        else:
            return "Brak ocen"


class Discount(models.Model):
    code = models.CharField(max_length=100)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.code + str(self.value)


class Order(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    delivery = models.CharField(max_length=100)
    products = models.ManyToManyField("Product", through="OrderedProducts")
    discount = models.ForeignKey(Discount, blank=True, null=True, on_delete=models.PROTECT)

    def get_total_price(self):
        total = 0
        ordered_products = OrderedProducts.objects.filter(order=self)

        for ordered_product in ordered_products:
            total += ordered_product.amount * ordered_product.product.price
        return total

    def get_total_price_after_discount(self):
        total = self.get_total_price()
        if self.discount is not None:
            total = total * (100 - self.discount.value) / 100
        return total

    def get_all_products(self):
        ordered_products = OrderedProducts.objects.filter(order=self)
        return list(ordered_products)

    def __str__(self):
        return self.name


class OrderedProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)


class Complaint(models.Model):
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return self.message[0:50]


class Opinion(models.Model):
    comment = models.CharField(max_length=1000)
    grade = models.IntegerField(default=1, validators=[MaxValueValidator(10), MinValueValidator(1)])
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.grade) + "  " + self.comment[0:50]
