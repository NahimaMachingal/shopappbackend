#shop/urls.py
from django.urls import path
from . import views
from .views import *

urlpatterns = [

    path('users/', UserListView.as_view(), name='user-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/add/', ProductCreateView.as_view(), name='product-add'),
    path("admin/orders/", AdminOrderListView.as_view(), name="admin-order-list"),
    path("admin/orders/<int:order_id>/update/", UpdateOrderStatusView.as_view(), name="update_order_status"),
]