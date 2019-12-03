from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
# Create your views here.

products = [
    {"name": "Szklana pułapka", "description": "Film akcji", "author": "Will Smith", "price": 100, "id": 1},
    {"name": "Fifa20", "description": "Gra sportowa", "author": "EA Sports", "price": 60, "id": 2},
    {"name": "Wybawiciel", "description": "Książka (kryminał)", "author": "Jo Nesbo", "price": 50, "id": 3},
]


def index(request, imie):
    return render(request, "sklep/glowna.html",
                  {"imie_klienta": imie})
def main_site(request):
    return render(request, "sklep/main_site.html")

def product_list(request):
    products = Product.objects.order_by('id')
    context = {'products':products}
    return render(
        request,
        "sklep/list.html",
        context
    )


def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product':product}
    return render(
        request,
        "sklep/product_details.html",
        context)
