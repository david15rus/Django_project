from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Products, Category


class IndexViewTestCase(TestCase):
    def test_status(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_redirect(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.context_data['title'], 'Store - Главная')

    def test_used_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def test_status(self):
        response = self.client.get(reverse('products:index'))
        self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_title(self):
        response = self.client.get(reverse('products:index'))
        self.assertEquals(response.context_data['title'], 'Store - Каталог')

    def test_used_template(self):
        response = self.client.get(reverse('products:index'))
        self.assertTemplateUsed(response, 'products/products.html')

    def test_pagination(self):
        products = list(Products.objects.all())
        response = self.client.get(reverse('products:index'))
        self.assertEquals(list(response.context_data['object_list']), products[:3])


class CategoriesTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def setUp(self):
        self.path = reverse('products:category', args=(1,))

    def test_status(self):
        response = self.client.get(self.path)
        self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_title(self):
        response = self.client.get(self.path)
        self.assertEquals(response.context_data['title'], 'Store - Каталог')

    def test_used_template(self):
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_category_filter(self):
        category = Category.objects.first()
        products = Products.objects.all()
        response = self.client.get(self.path)
        self.assertEquals(
            list(response.context_data['object_list']),
            list(products.filter(category_id=category.id))
        )

