from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import ListView

from .forms import *
from .models import *
from django.utils import timezone


def home(request):
    context = {}
    limit = 10
    posts = Post.objects.all()[:limit]

    if not request.user.is_superuser:
        posts = Post.objects.filter(is_draft=False, published_date__lte=timezone.now())[:limit]

    context['posts'] = posts
    return render(request, 'goods/home.html', context)


def categories(request):
    context = {
        'categories': Category.objects.all()
    }
    return render(request, 'goods/category.html')


def basket(request):
    return render(request, 'goods/basket.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'goods/u_login.html', {'form': form})


from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def post(request):
    return render(request, 'goods/post.html')


class Search(ListView):
    template_name = 'search/search.html'
    context_object_name = 'posts'
    paginate_by = 5
    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context