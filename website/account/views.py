from django.shortcuts import render, redirect
from django.contrib.auth import logout
from urllib.parse import urlparse, urlunparse
from django.conf import settings
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordContextMixin, LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import LoginForm

UserModel = get_user_model()


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Авторизация")
    #     return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')




def logout_user(request):
    logout(request)
    return redirect('login')

# class LogoutView(SuccessURLAllowedHostsMixin, TemplateView):
#     next_page = None
#     redirect_field_name = REDIRECT_FIELD_NAME
#     template_name = 'logged_out.html'
#     extra_context = None
#     @method_decorator(never_cache)
#     def dispatch(self, request, *args, **kwargs):
#         auth_logout(request)
#         next_page = self.get_next_page()
#         if next_page:
#             # Redirect to this page until the session has been cleared.
#             return HttpResponseRedirect(next_page)
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         """Logout may be done via POST."""
#         return self.get(request, *args, **kwargs)
#
#     def get_next_page(self):
#         if self.next_page is not None:
#             next_page = resolve_url(self.next_page)
#         elif settings.LOGOUT_REDIRECT_URL:
#             next_page = resolve_url(settings.LOGOUT_REDIRECT_URL)
#         else:
#             next_page = self.next_page
#
#         if (self.redirect_field_name in self.request.POST or
#                 self.redirect_field_name in self.request.GET):
#             next_page = self.request.POST.get(
#                 self.redirect_field_name,
#                 self.request.GET.get(self.redirect_field_name)
#             )
#             url_is_safe = url_has_allowed_host_and_scheme(
#                 url=next_page,
#                 allowed_hosts=self.get_success_url_allowed_hosts(),
#                 require_https=self.request.is_secure(),
#             )
#             # Security check -- Ensure the user-originating redirection URL is
#             # safe.
#             if not url_is_safe:
#                 next_page = self.request.path
#         return next_page
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         current_site = get_current_site(self.request)
#         context.update({
#             'site': current_site,
#             'site_name': current_site.name,
#             'title': _('Logged out'),
#             **(self.extra_context or {})
#         })
#         return context
#
#
# def logout_then_login(request, login_url=None):
#     """
#     Log out the user if they are logged in. Then redirect to the login page.
#     """
#     login_url = resolve_url(login_url or settings.LOGIN_URL)
#     return LogoutView.as_view(next_page=login_url)(request)
#
#
# def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
#     """
#     Redirect the user to the login page, passing the given 'next' page.
#     """
#     resolved_url = resolve_url(login_url or settings.LOGIN_URL)
#
#     login_url_parts = list(urlparse(resolved_url))
#     if redirect_field_name:
#         querystring = QueryDict(login_url_parts[4], mutable=True)
#         querystring[redirect_field_name] = next
#         login_url_parts[4] = querystring.urlencode(safe='/')
#
#     return HttpResponseRedirect(urlunparse(login_url_parts))
#
