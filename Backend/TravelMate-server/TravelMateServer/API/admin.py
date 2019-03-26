from django.contrib import admin
from .models import UserProfile, Language, Interest, Rate, Invitation, Message, Application, Global, Trip, Country, City, Advertisement

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Language)
admin.site.register(Interest)
admin.site.register(Rate)
admin.site.register(Invitation)
admin.site.register(Message)
admin.site.register(Application)
admin.site.register(Global)
admin.site.register(Trip)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Advertisement)