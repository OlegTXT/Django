from django.urls import path
from shop.views import category_list, Category_detail, add_to_cart, cart

urlpatterns = [
    path('category-list/', category_list, name='category_list'),
    path('category-detail/<int:pk>/', Category_detail.as_view(), name='category_detail'),
    path('add-card/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
]
