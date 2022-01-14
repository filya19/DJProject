from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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


class LoginForm(forms.Form):
    username = forms.CharField(label=u'Имя пользователя')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())
