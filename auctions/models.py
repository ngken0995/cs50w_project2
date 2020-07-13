from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

category_choices = [
    ('Arts', 'Arts, Crafts and Sewing'),
    ('Cars', 'Automotive parts'),
    ('Gene', 'General'),
    ('Toys', 'Toys')
    ]

class Auctions(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(choices=category_choices, max_length=4, default='Arts')
    image = models.URLField(blank=True, null=True)

class Bids(models.Model):
    item = models.ForeignKey(Auctions, on_delete=models.CASCADE)
    bidPrice = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)


class Comments(models.Model):
    item = models.ForeignKey(Auctions, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)

class Wishlists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creater')
    item = models.ForeignKey(Auctions, on_delete=models.CASCADE)
