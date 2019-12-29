from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_site),
    path('products/', views.product_list),
    path('product/<int:product_id>', views.product_details),
    path("order/", views.order),
    path("order/<int:order_id>", views.order_details),
    path("complaint/", views.complaint),
    path("complaint/<int:complaint_id>", views.complaint_details),
    path("cart/", views.cart),
    path("cart/add/", views.add_to_cart),
    path("cart/delete/", views.delete_from_cart),
    path("cart/change/", views.change_cart),
    path("product_details/", views.product_details)
]
