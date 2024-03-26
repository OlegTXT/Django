from django.urls import path
from shop.views import category_list, Category_detail, add_to_cart, cart, checkout

urlpatterns = [
    path('', category_list, name='category_list'),
    path('<int:pk>/', Category_detail.as_view(), name='category_detail'),
    path('add-card/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
]
