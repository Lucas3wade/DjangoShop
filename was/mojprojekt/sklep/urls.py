from django.urls import path
from . import views

urlpatterns = [
    path('widok/', views.index),
    path('widok/<str:tekst>', views.index),
    path('glowna/<str:imie>', views.index),
    path('products/', views.product_list),
    path('product/<int:product_id>', views.product_details),
    path('', views.main_site)

]
