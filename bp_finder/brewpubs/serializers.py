from django.contrib.auth import get_user_model
from rest_framework import serializers


from . import models

User = get_user_model()


"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'email')
"""


class BrewpubSerializer(serializers.ModelSerializer):
    brewpub_beers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Brewpub
        fields = ('id',
                  'name',
                  'address',
                  'telephone',
                  'website',
                  'hours',
                  'brewpub_beers')
        extra_kwargs = {
            'is_admin': {'write_only': True}
        }


class BeerSerializer(serializers.ModelSerializer):
    brewpub = BrewpubSerializer(many=True, read_only=True)

    class Meta:
        model = models.Beer
        fields = ('id',
                  'name',
                  'beer_type',
                  'description',
                  'brewpub',)
        extra_kwargs = {
            'is_admin': {'write_only': True}
        }


class ReviewSerializer(serializers.ModelSerializer):
    brewpub = BrewpubSerializer(many=True, read_only=True)
    beer = BeerSerializer(many=True, read_only=True)
    #  User = get_user_model()

    class Meta:
        model = models.Review
        fields = (
            'id',
            'brewpub',
            'beer',
            'username',
            'email',
            'comment',
            'rating',
            'created_at'
        )
        lookup_field = 'id'
