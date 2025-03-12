from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]
