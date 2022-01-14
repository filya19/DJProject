from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', views.post, name="post"),
    path('categories', views.categories, name='category'),
    path('basket', views.basket, name="backet"),
    path('registration', views.signup, name='registration'),
    path('u_login', views.user_login, name='login'),
    path('post', views.post, name='post'),
]
