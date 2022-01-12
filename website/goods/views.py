from django.shortcuts import render


def home(request):
    return render(request, 'goods/home.html')


def categories(request):
    return render(request, 'goods/cats.html')


def login(request):
    return render(request, 'goods/login.html')


def basket(request):
    return render(request, 'goods/basket.html')


def registration(request):
    return render(request, 'goods/registration.html')