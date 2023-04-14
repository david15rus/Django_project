from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

from products.models import Basket
from users.forms import UserLogin, UserRegistration, UserProfile
from users.models import User
from common.view import TitleCommonMixin


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

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        context['basket'] = Basket.objects.filter(user=self.object)
        return context
