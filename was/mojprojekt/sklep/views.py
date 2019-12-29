from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .forms import OrderForm, ComplaintForm, OpinionForm
from .models import Product, Order, Complaint, OrderedProducts, Discount, Opinion


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
    comments = product.get_all_opinions()
    grade = product.get_grade()

    if request.method == "POST":
        form = OpinionForm(request.POST)
        if form.is_valid():
            opinion = Opinion(
                comment=form.cleaned_data['comment'],
                grade=form.cleaned_data['grade'],
                product=product
            )
            opinion.save()
            return HttpResponseRedirect('/product/' + str(product_id))
    else:
        form = OpinionForm()
    context = {'product': product, 'comments': comments, 'grade': grade, 'form': form}
    return render(request, 'sklep/product_details.html', context)


def order(request):
    products = _get_zipped_products_amounts(request)
    total_price = 0
    for product, amount in products:
        total_price = total_price + product.price * amount
    products = _get_zipped_products_amounts(request)
    if request.method == "POST":
        form = OrderForm(request.POST)
        discount_code = request.POST['discount']
        try:
            discount = Discount.objects.get(code=discount_code)
        except Discount.DoesNotExist:
            discount = None

        if form.is_valid():
            order = Order(
                name=form.cleaned_data['name'],
                address=form.cleaned_data['address'],
                delivery=form.cleaned_data['delivery'],
                discount=discount
            )
            order.save()

            for product, amount in products:
                ordered_product = OrderedProducts(
                    product=product, order=order, amount=amount
                ).save()
                request.session['cart'] = []
                request.session['cart_amounts'] = []

            return HttpResponseRedirect('/order/' + str(order.id))
    else:
        form = OrderForm()
    return render(request, 'sklep/order_form.html', {
        "form": form, "products": products, "total_price": total_price
    })


def order_details(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    ordered_products = order.get_all_products()
    total_price = order.get_total_price()
    total_price_after_discount = order.get_total_price_after_discount()
    if order.discount is not None:
        order_discount_code = order.discount.code
        order_discount_value = order.discount.value
    else:
        order_discount_code = "brak"
        order_discount_value = 0
    context = {'ordered_products': ordered_products,
               'total_price': total_price,
               'total_price_after_discount': total_price_after_discount,
               'order_discount_code': order_discount_code,
               'order_discount_value': order_discount_value
               }
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


def cart(request):
    products = _get_zipped_products_amounts(request)
    total_price = 0
    for product, amount in products:
        total_price = total_price + product.price * amount
    products = _get_zipped_products_amounts(request)
    return render(request, "sklep/cart.html", {"products": products, "total_price": total_price})


def add_to_cart(request):
    if request.method == "POST":
        if 'cart' and 'cart_amounts' not in request.session:
            request.session['cart'] = []
            request.session['cart_amounts'] = []

        item_id = request.POST['item_id']

        if item_id in request.session['cart']:
            index = request.session['cart'].index(item_id)
            request.session['cart_amounts'][index] = request.session['cart_amounts'][index] + 1
        else:
            request.session['cart'].append(item_id)
            request.session['cart_amounts'].append(1)
        request.session.modified = True

    return HttpResponseRedirect('/cart')


def delete_from_cart(request):
    if request.method == "POST":
        item_id = request.POST['item_id']
        index = request.session['cart'].index(item_id)
        request.session['cart'].pop(index)
        request.session['cart_amounts'].pop(index)
        request.session.modified = True

    return HttpResponseRedirect('/cart')


def change_cart(request):
    if request.method == "POST":
        item_id = request.POST['item_id']
        amount = request.POST['amount']
        index = request.session['cart'].index(item_id)
        request.session['cart_amounts'][index] = int(amount)
        request.session.modified = True

    return HttpResponseRedirect('/cart')


def _get_products_in_cart(request):
    products_in_cart = []
    for item_id in request.session.get('cart', []):
        product = Product.objects.get(pk=item_id)
        products_in_cart.append(product)
    return products_in_cart


def _get_amounts_of_products_in_cart(request):
    amounts_of_products_in_cart = []
    for amount in request.session.get('cart_amounts', []):
        amounts_of_products_in_cart.append(amount)
    return amounts_of_products_in_cart


def _get_zipped_products_amounts(request):
    products_in_cart = _get_products_in_cart(request)
    amounts_of_products_in_cart = _get_amounts_of_products_in_cart(request)
    return zip(products_in_cart, amounts_of_products_in_cart)
