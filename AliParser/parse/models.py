from django.db import models


class Seller(models.Model):
    url = models.CharField(max_length=124, unique=True)


class Product(models.Model):
    num = models.CharField(max_length=16, unique=True)
    info = models.TextField()
