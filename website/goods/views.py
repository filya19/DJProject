from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *
from django.utils import timezone


def home(request):
    context = {}
    limit = 10
    posts = Post.objects.all()[:limit]
    context['posts'] = posts
    return render(request, 'goods/home.html', context)


def categories(request):
    context = {
        'categories': Category.objects.all()
    }
    return render(request, 'goods/category.html', context)


def basket(request):
    return render(request, 'goods/basket.html')


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#     else:
#         form = LoginForm(request.POST)
#     return render(request, 'goods/u_login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def post(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, 'goods/post.html', context)


class Search(ListView):
    template_name = 'search/search.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(
            Q(title__icontains=self.request.GET.get('s')))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


class PostsByCategory(ListView):
    template_name = 'goods/home.html'
    context_object_name = 'posts'
    allow_empty = True

    def get_queryset(self):
        return Post.objects.filter(category_slug=self.kwargs['slug'])

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


# class PostCreateNew(LoginRequiredMixin,CreateView):
#     model = Post
#     form_class =
#     template_name = 'createpost.html'
#     success_url = reverse_lazy('home')
#     login_url =reverse_lazy ('login')
#     raise_exception = True
#     fields = ['title', 'category', 'description', 'phone', 'image', 'city']


