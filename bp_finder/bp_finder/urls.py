"""bp_finder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls',
                           namespace='rest_framework')),
    # these don't have templates that work.
    #url(r'^login/', login_view, name='login'),
    #url(r'^logout/', logout_view, name='logout'),
    #url(r'^register/', register_view, name='register'),
    #url(r'^api/v1/brewpubs/', include('brewpubs.urls', namespace='brewpub')),
    url(r'^api/v1/', include('brewpubs.urls', namespace='apiv1')),
    url(r'^api/users/', include('accounts.urls', namespace='users-api')),
]
