from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .forms import OrderForm, ComplaintForm
from .models import Product, Order, Complaint


# Create your views here.

def main_site(request):
    return render(request, "sklep/main_site.html")


def product_list(request):
    products = Product.objects.order_by('id')
    context = {'products': products}
    return render(
        request,
        "sklep/list.html",
        context
    )


def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(
        request,
        "sklep/product_details.html",
        context)


def order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order(
                name=form.cleaned_data['name'],
                address=form.cleaned_data['address'],
                delivery=form.cleaned_data['delivery']
            )
            order.save()
            return HttpResponseRedirect('/order/' + str(order.id))
    else:
        form = OrderForm()
    return render(request, 'sklep/order_form.html', {
        "form": form
    })


def order_details(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    ordered_products = order.get_all_products()
    total_price = order.get_total_price()
    context = {'ordered_products': ordered_products, 'total_price': total_price}
    return render(
        request,
        "sklep/order_details.html",
        context)


def complaint(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = Complaint(
                name=form.cleaned_data['name'],
                message=form.cleaned_data['message'],
            )
            complaint.save()
            return HttpResponseRedirect('/complaint/' + str(complaint.id))
    else:
        form = ComplaintForm()
    return render(request, 'sklep/complaint_form.html', {
        "form": form
    })


def complaint_details(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id)
    context = {'complaint': complaint}
    return render(
        request,
        "sklep/complaint_details.html",
        context)
