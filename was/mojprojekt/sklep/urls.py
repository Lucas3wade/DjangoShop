from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_site),
    path('products/', views.product_list),
    path('product/<int:product_id>', views.product_details),
    path("order/", views.order),
    path("order/<int:order_id>", views.order_details),
    path("complaint/", views.complaint),
    path("complaint/<int:complaint_id>", views.complaint_details)
]
