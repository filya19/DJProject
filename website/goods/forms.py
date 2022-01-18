from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=32, help_text='Введите логин', label='Логин')
    first_name = forms.CharField(max_length=32, help_text='Введите ваше Имя', label='Имя')
    last_name = forms.CharField(max_length=32, help_text='Введите вашу Фамилию', label='Фамилия')
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput,
                                help_text='Введите тот же пароль, что и раньше, для проверки.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class PostCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"

    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'image', 'status', 'phone', 'city', 'price']
        widgets = {
            'author':forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),

        }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateForm, self).form_valid(form)


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ваше имя"
        })
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Оставьте комментарий"
        })
    )
