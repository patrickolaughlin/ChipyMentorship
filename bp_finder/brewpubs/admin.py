from django.contrib import admin
from django.contrib.auth import get_user_model

from brewpubs.models import Brewpub, Review, Beer

User = get_user_model()

admin.site.register(Brewpub)
admin.site.register(Review)
admin.site.register(Beer)
#  admin.site.register(User)
