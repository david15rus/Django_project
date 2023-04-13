from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=150)
    descriptions = models.TextField(null=True, blank=None)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=150)
    descriptions = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return f"Продукт: {self.name} | Категории: {self.category}"


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(product.sum() for product in self)

    def total_qty(self):
        return sum(product.quantity for product in self)


class Basket(models.Model):
    quantity = models.PositiveSmallIntegerField(default=0)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина {self.user.username} | Продукт {self.product.name}"

    def sum(self):
        return self.product.price * self.quantity
