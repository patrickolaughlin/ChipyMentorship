from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    user = models.ForeignKey(User)
    comment = models.TextField(blank=True, default='')
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0.rating} by {0.user.username}'.format(self)


class Brewpub(models.Model):
    name = models.CharField(max_length=30, unique=True)
    address = models.TextField()
    telephone = models.CharField(max_length=10)
    website = models.URLField()
    hours = JSONField()
    review = models.ManyToManyField(Review, related_name='brewpub_reviews', blank=True)

    def __str__(self):
        return self.name


class Beer(models.Model):
    BEER_TYPES = (
        ('Pilsner', 'Pilsner'),
        ('Wheat', 'Wheat'),
        ('Brown Ale', 'Brown Ale'),
        ('Pale Ale', 'Pale Ale'),
        ('India Pale Ale', 'India Pale Ale'),
        ('Bock', 'Bock'),
        ('Porter', 'Porter'),
        ('Stout', 'Stout'),
    )

    name = models.CharField(max_length=30)
    beer_type = models.CharField(max_length=30, choices=BEER_TYPES)
    description = models.TextField()
    brewpub = models.ManyToManyField(Brewpub, related_name='brewpub_beers', blank=True)
    review = models.ManyToManyField(Review, related_name='beer_reviews', blank=True)

    def __str__(self):
        return self.name
