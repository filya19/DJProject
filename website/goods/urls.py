from django.urls import path
from . import views
from .views import Search

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', views.post, name="post"),
    path('categories/', views.categories, name='category'),
    path('basket/', views.basket, name="basket"),
    path('registration/', views.signup, name='registration'),
    path('post/', views.post, name='post'),
    path('search/', Search.as_view(), name='search'),
]
