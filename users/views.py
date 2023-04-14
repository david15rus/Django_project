from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

from products.models import Basket
from users.forms import UserLogin, UserRegistration, UserProfile
from users.models import User


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLogin


def user_login(request):
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLogin()
    context = {'form': form}
    return render(request, 'users/login.html', context)


class RegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistration
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = "Регистрация прошла успешно!"

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data()
        context['title'] = 'Store - Регистрация'
        return context


class ProfileView(UpdateView):
    model = User
    form_class = UserProfile
    template_name = 'users/profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        context['title'] = 'Store - Профиль'
        context['basket'] = Basket.objects.filter(user=self.object)
        return context
