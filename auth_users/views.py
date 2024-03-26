from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def auth_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('category_list')

        else:
            messages.add_message(request, messages.WARNING, 'Auth failed')
            return redirect('auth_login')
    return render(request, 'auth_users/login.html')


def auth_logout(request):
    logout(request)
    return redirect('auth_login')