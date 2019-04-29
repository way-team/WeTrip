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
from django.urls import include, path, re_path
from django.conf.urls import url
from rest_framework import routers
from TravelMateServer.API import views
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', obtain_auth_token),
    path('getUserByToken/', views.GetUserView.as_view()),
    path('getUserById/', views.GetUserByIdView.as_view()),
    url('^users/(?P<username>.+)/$', views.UserList.as_view()),
    path('rate/', views.RateUser.as_view()),
    path('trips/', views.AvailableTripsList.as_view()),
    path('trips/myTrips/', views.MyTripsList.as_view()),
    path('trips/search/', views.AvailableTripsSearch.as_view()),
    path('list-cities/', views.ListCities.as_view()),
    path('createTrip/', views.CreateTrip.as_view()),
    path('getFriends/', views.GetFriendsView.as_view()),
    path('getPending/', views.GetPendingView.as_view()),
    path('sendInvitation/', views.SendInvitation.as_view()),
    path('acceptFriend/', views.AcceptFriend.as_view()),
    path('rejectFriend/', views.RejectFriend.as_view()),
    path('getDiscoverPeople/', views.DiscoverPeopleView.as_view()),
    url('^getTrip/(?P<trip_id>.+)/$', views.GetTripView.as_view()),
    path('editTrip/', views.EditTripView.as_view()),
    path('applyTrip/', views.ApplyTripView.as_view()),
    path('acceptApplication/', views.AcceptApplicationView.as_view()),
    path('rejectApplication/', views.RejectApplicationView.as_view()),
    path('dashboard/', views.DashboardData.as_view(), name='dashboard'),
    path(
        'messages/<int:sender>/<int:receiver>/',
        views.message_list,
        name='message-detail'),
    path('messages/', views.message_list, name='message-list'),
    path('paid/', views.SetUserToPremium.as_view()),
    path('register/', views.RegisterUser.as_view()),
    path('list-languages/', views.ListLanguages.as_view()),
    path('list-interests/', views.ListInterest.as_view()),
] + static(
    settings.STATIC_URL, document_root=settings.STATICFILES_STORAGE)
