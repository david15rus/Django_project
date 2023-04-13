from django.urls import path

from users.views import user_login, register, profile, user_logout

app_name = 'users'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', user_logout, name='logout')
]