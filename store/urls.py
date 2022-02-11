from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('navbar', navbar, name="navbar"),
    path('footer', footer, name="footer"),
    path('store/', ProductList.as_view(), name='product'),
    path('category/<str:slug>/', CategoryProductList.as_view(), name='category'),
    path('store/<int:id>/', product_detail, name='product-detail'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>', cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>', cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>', cart_update, name='cart_update'), 
    path('checkout/', checkout, name='checkout'),
    path('to_bank/<int:order_id>/', to_bank, name='to_bank'), 
    path('callback/', callback, name='callback'), 
  ]
