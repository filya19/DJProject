from django.urls import path
from .views import *


urlpatterns = [
    path('', home),
    path('categories', categories),
    # path('u_login', u_login, name='login'),
    path('basket', basket, name="backet"),
    path('registration', registration, name='register'),
    path('u_login', user_login, name='login')
]
