from TravelMateServer.API.serializers import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import UserProfile, City
from django.contrib.auth.models import User
from rest_framework import authentication, generics
from rest_framework.permissions import IsAuthenticated


class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        user = tk.user
        userProfile = UserProfile.objects.get(user=user)

        return Response(UserProfileSerializer(userProfile, many=False).data)


class UserList(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (authentication.TokenAuthentication,
                              authentication.SessionAuthentication)

    def get(self, request, *args, **kwargs):
        """
        Get the user by his username
        """
        username = kwargs.get('username')
        userProfile = User.objects.get(username=username).userprofile
        return Response(UserProfileSerializer(userProfile, many=False).data)

class ListCities(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (authentication.TokenAuthentication,
                              authentication.SessionAuthentication)

    def get(self, request):
        
        
        cities = City.objects.all()
        return Response(CitySerializer(cities, many=True).data)

class CreateTrip(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (authentication.TokenAuthentication,
                              authentication.SessionAuthentication)

    def post(self, request):

        #GET TRIP DATA
        #Comment the following line and remove the comment from one after that to test with Postman
        username = request.user.username
        #username= request.data.get('username','')
        user = User.objects.get(username=username).userprofile
        title = request.data.get('title', '')
        description = request.data.get('description', '')
        startDate = request.data.get('start_date', '')
        endDate = request.data.get('end_date', '')
        tripType = request.data.get('trip_type', '')
        image = request.data.get('image', '')
        #GET CITY DATA
        cityId = request.data.get('city')
        #CREATE AND SAVE TRIP
        trip = Trip(user=user, title=title, description=description, startDate=startDate, endDate=endDate,
        tripType=tripType, image=image)
        trip.save()

        

        #GET CITY AND ADD TRIP
        city = City.objects.get(pk=cityId)
        city.trips.add(trip)


        return Response(TripSerializer(trip, many=False).data)