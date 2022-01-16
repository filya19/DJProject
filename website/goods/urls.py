from django.urls import path
from . import views
from .views import Search, PostCreateNew

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:slug>/', views.post, name="post"),
    path('categories', views.categories, name='category'),
    path('categories/<str:slug>/', views.PostsByCategory.as_view, name='category'),
    path('basket', views.basket, name="backet"),
    path('registration', views.signup, name='registration'),
    path('u_login', views.user_login, name='login'),
    path('post', views.post, name='post'),
    path('search', Search.as_view(), name='search'),

]
