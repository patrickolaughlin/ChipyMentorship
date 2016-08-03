from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^brewpubs/$', views.ListCreateBrewpub.as_view(), name='brewpub_list'),
    url(r'^brewpubs/(?P<pk>\d+)/$', views.RetrieveUpdateDestroyBrewpub.as_view(),
        name='brewpub_detail'),
    url(r'^brewpubs/(?P<brewpub_pk>\d+)/reviews/$', views.ListCreateBrewpubReview.as_view(),
        name='brewpub_review_list'),
    url(r'^beer/$', views.ListCreateBeer.as_view(), name='beer_list'),
    url(r'^beer/(?P<pk>\d+)/$', views.RetrieveUpdateDestroyBeer.as_view(),
        name='beer_detail'),
    url(r'^beer/(?P<beer_pk>\d+)/reviews/$', views.ListCreateBeerReview.as_view(),
        name='beer_review_list'),
    url(r'^reviews/$', views.ListUsersReviews.as_view(),
        name='user_reviews'),
    url(r'^reviews/(?P<pk>\d+)/$', views.RetrieveUpdateDestroyReview.as_view(),
        name='user_detail_review'),
]
