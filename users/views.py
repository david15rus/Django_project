from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.view import TitleCommonMixin
from users.forms import UserLogin, UserProfile, UserRegistration
from users.models import EmailVerification, User


class UserLoginView(TitleCommonMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLogin
    title = 'Store - Авторизация'


class RegistrationView(TitleCommonMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistration
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = "Регистрация прошла успешно!"
    title = 'Store - Регистрация'


class ProfileView(TitleCommonMixin, UpdateView):
    model = User
    form_class = UserProfile
    template_name = 'users/profile.html'
    title = 'Store - Профиль'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TitleCommonMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Store - Подтверждение электронной почты'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(
            user=user,
            code=code
        )
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(self, request, *args, **kwargs)
        else:
            HttpResponseRedirect(reverse('index'))
