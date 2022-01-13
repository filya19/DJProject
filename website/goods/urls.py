from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('categories', categories, name='cats'),
    path('basket', basket, name="backet"),
    path('registration', signup, name='registration'),
    path('u_login', user_login, name='login')
]
