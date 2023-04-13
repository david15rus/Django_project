from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

from products.models import Basket
from users.forms import UserLogin, UserRegistration, UserProfile


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


def register(request):
    if request.method == 'POST':
        form = UserRegistration(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistration()
    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfile(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))

    else:
        form = UserProfile(instance=request.user)
    context = {
        'title': 'Store - Профиль',
        'form': form,
        'basket': Basket.objects.filter(user=request.user)
    }
    return render(request, 'users/profile.html', context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))