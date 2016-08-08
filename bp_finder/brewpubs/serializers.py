from django.contrib.auth import get_user_model
from rest_framework import serializers


from . import models

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        fields = (
            'id',
            'user',
            'comment',
            'rating',
            'created_at'
        )


class BrewpubSerializer(serializers.ModelSerializer):
    brewpub_beers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = models.Brewpub
        fields = ('id',
                  'name',
                  'address',
                  'telephone',
                  'website',
                  'hours',
                  'brewpub_beers',
                  'reviews')
        extra_kwargs = {
            'is_admin': {'write_only': True}
        }


class BeerSerializer(serializers.ModelSerializer):
    brewpub = BrewpubSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = models.Beer
        fields = ('id',
                  'name',
                  'beer_type',
                  'description',
                  'brewpub',
                  'reviews',)
        extra_kwargs = {
            'is_admin': {'write_only': True}
        }
