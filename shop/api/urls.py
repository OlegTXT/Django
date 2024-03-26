from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop.api import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'products', views.ProductViewSet, basename='products')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]