from django.urls import path
from auth_users.views import auth_login, auth_logout

urlpatterns = [
    path('login/', auth_login, name='auth_login'),
    path('logout/', auth_logout, name='auth_logout'),
]