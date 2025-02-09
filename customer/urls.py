
from django.urls import path
from . import views
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('api/token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('cart/', CartItemListView.as_view(), name='cart-list'),
    path('cart/add/', CartItemCreateView.as_view(), name='cart-add'),
    path('cart/update/', CartItemUpdateView.as_view(), name='cart-update'),
    path('cart/remove/<int:product_id>/', CartItemRemoveView.as_view(), name='cart-remove'),
    path('address/add/', SubmitAddressView.as_view(), name='address-add'),
    path('order/submit/', SubmitOrderView.as_view(), name='submit-order'),  # New order submission endpoint
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('rating/submit/', SubmitRatingView.as_view(), name='submit-rating'),
]
