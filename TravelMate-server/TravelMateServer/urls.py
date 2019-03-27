"""TravelMateServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.contacts, name='contacts')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='contacts')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from TravelMateServer.API import views
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', obtain_auth_token),
    path('getUserByToken/', views.GetUserView.as_view()),
    path('list-cities/', views.ListCities.as_view()),
    path('createTrip/', views.CreateTrip.as_view()),
    url('^users/(?P<username>.+)/$', views.UserList.as_view()),
    path('getFriends/', views.GetFriendsView.as_view()),
    path('getDiscoverPeople/', views.DiscoverPeopleView.as_view()),
]
