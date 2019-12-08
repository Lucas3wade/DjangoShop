from django.contrib import admin

# Register your models here.

from .models import Product, Order, OrderedProducts, Complaint

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderedProducts)
admin.site.register(Complaint)