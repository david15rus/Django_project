from http import HTTPStatus
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.forms import UserRegistration, User, EmailVerification


class UserLoginTestCase(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse('users:login'))

    def test_status(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_title(self):
        self.assertEqual(self.response.context_data['title'], 'Store - Авторизация')


class UserRegistrationTestCase(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'Давид',
            'last_name': 'Авдонин',
            'username': 'david15russ',
            'email': 'uck15@bk.ru',
            'password1': '25052001d',
            'password2': '25052001d',
        }
        self.path = reverse('users:register')

    def test_status(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_title(self):
        response = self.client.get(self.path)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')

    def test_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(days=2)).date(),
        )

    def test_user_registration_post_error(self):
        username = self.data['username']
        User.objects.create(username=username)
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        error_message = 'Пользователь с таким именем уже существует.'
        self.assertContains(response, error_message, html=True)