from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum


class User(AbstractUser):
    @property
    def balance(self):
        amount = self.transaction.all().aggregate(Sum("amount"))["amount__sum"]
        if amount:
            return amount
        return 0


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    title = models.CharField(max_length=200)

    def __str__(self):
        return str(self.title)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction")
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    organization = models.CharField(max_length=200)

    @property
    def category_name(self):
        return self.category.title

    @category_name.setter
    def category_name(self, value):
        self.category.title = value
