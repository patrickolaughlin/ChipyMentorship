from django.contrib.auth import get_user_model

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from brewpubs.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

from . import models
from . import serializers


User = get_user_model()


class ListCreateBrewpub(generics.ListCreateAPIView):
    queryset = models.Brewpub.objects.all()
    serializer_class = serializers.BrewpubSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RetrieveUpdateDestroyBrewpub(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Brewpub.objects.all()
    serializer_class = serializers.BrewpubSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ListCreateBeer(generics.ListCreateAPIView):
    queryset = models.Beer.objects.all()
    serializer_class = serializers.BeerSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RetrieveUpdateDestroyBeer(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Beer.objects.all()
    serializer_class = serializers.BeerSerializer
    permission_classes = (IsAdminOrReadOnly,)


# =========================================================

class ListCreateBrewpubReview(generics.ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return self.queryset.filter(brewpub_reviews=self.kwargs.get('brewpub_pk'))

    def perform_create(self, serializer):
        brewpub = get_object_or_404(
            models.Brewpub, pk=self.kwargs.get('brewpub_pk'))
        #  need to check that submitted user is actual user
        if self.request.user == serializer.validated_data['user']:
            if serializer.is_valid():
                serializer.save()
                new_review = get_object_or_404(models.Review, pk=serializer.data['id'])
                brewpub.review.add(new_review)
        else:
            raise PermissionDenied()


class RetrieveUpdateDestroyBrewpubReview(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            brewpub_id=self.kwargs.get('brewpub_pk'),
            pk=self.kwargs.get('pk'))

    def perform_update(self, serializer):
        if serializer.is_valid:
            serializer.save()

    def perform_destroy(self, serializer):
        serializer.delete()


# trying to get the correct review for a beer:
class ListBeerReview(generics.ListAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return self.queryset.filter(beer_reviews=self.kwargs.get('beer_pk'))


class ListCreateBeerReview(generics.ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return self.queryset.filter(beer_reviews=self.kwargs.get('beer_pk'))

    def perform_create(self, serializer):
        beer = get_object_or_404(
            models.Beer, pk=self.kwargs.get('beer_pk'))
        if self.request.user == serializer.validated_data['user']:
            if serializer.is_valid():
                serializer.save()
                new_review = get_object_or_404(models.Review, pk=serializer.data['id'])
                beer.review.add(new_review)
        else:
            raise PermissionDenied()


class ListUsersReviews(generics.ListAPIView):
    #  List all reviews by one user:
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)


class RetrieveUpdateDestroyReview(generics.RetrieveUpdateDestroyAPIView):
    #  One review by one user
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            pk=self.kwargs.get('pk'))

    def perform_update(self, serializer):
        if serializer.is_valid:
            serializer.save()

    def perform_destroy(self, serializer):
        serializer.delete()
