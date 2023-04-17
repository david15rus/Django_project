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


class ProductsViewTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def setUp(self):
        self.response = self.client.get(reverse('products:index'))

    def test_status(self):
        self.assertEquals(self.response.status_code, HTTPStatus.OK)

    def test_title(self):
        self.assertEquals(self.response.context_data['title'], 'Store - Каталог')

    def test_used_template(self):
        self.assertTemplateUsed(self.response, 'products/products.html')

    def test_pagination(self):
        products = list(Products.objects.all())
        response = self.client.get(reverse('products:paginator', args=(1,)))
        self.assertEquals(list(response.context_data['object_list']), products[:3])


class ProductsViewSortedTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']

    def setUp(self):
        self.path = reverse('products:category', args=(1,))
        self.response = self.client.get(self.path)

    def test_status(self):
        self.assertEquals(self.response.status_code, HTTPStatus.OK)

    def test_used_template(self):
        self.assertTemplateUsed(self.response, 'products/products.html')

    def test_sorting_by_category(self):
        category = Category.objects.first()
        products = Products.objects.all()
        self.assertEquals(
            list(self.response.context_data['object_list']),
            list(products.filter(category_id=category.id))
        )


class ProductToBasketTestCase(TestCase):
    fixtures = ['products.json', 'categories.json']

    def setUp(self):
        self.path = reverse('products:product_to_basket', args=(1,))

    def test_status(self):
        response = self.client.get(self.path)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
