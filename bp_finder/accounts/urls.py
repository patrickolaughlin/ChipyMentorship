from django.conf.urls import url

from .views import (
    UserCreateAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    )


urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^logout/$', UserLogoutAPIView.as_view(), name='logout'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
]
