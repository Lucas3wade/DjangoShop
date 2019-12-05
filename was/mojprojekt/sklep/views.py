from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .forms import OrderForm
from .models import Product, Order

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
def order_details(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    total_price = order.get_total_price()
    return HttpResponse(total_price)

def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product':product}
    return render(
        request,
        "sklep/product_details.html",
        context)

def order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                address = form.cleaned_data['address'],
                shipping_method = form.cleaned_data['shipping_method']
            )
            order.save()
            return HttpResponseRedirect('/order/' + str(order.id))
    else:
        form = OrderForm()
    return render(request, 'sklep/order_form.html', {
        "form":form
    })