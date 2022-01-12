from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('categories', categories),
    path('login', login, name='login'),
    path('basket', basket, name="backet"),
    path('registration', registration, name='register'),
]