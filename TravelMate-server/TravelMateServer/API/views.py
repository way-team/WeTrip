from TravelMateServer.API.serializers import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, filters
from .models import UserProfile, Trip, Invitation, City
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from datetime import datetime
from django.db.models import Q


def getUserByToken(request):
    key = request.data.get('token', '')
    tk = get_object_or_404(Token, key=key)
    user = tk.user

    return user

class GetUserView(APIView):
    def post(self, request):
        user = getUserByToken(request)
        userProfile = UserProfile.objects.get(user=user)

        return Response(UserProfileSerializer(userProfile, many=False).data)

class UserList(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,
                              SessionAuthentication)

    def get(self, request, *args, **kwargs):
        """
        Get the user by his username
        """
        username = kwargs.get('username')
        userProfile = User.objects.get(username=username).userprofile
        return Response(UserProfileSerializer(userProfile, many=False).data)

def getFriendsOrPending(user):
    friends = []
    pending = []

    sInvitations = Invitation.objects.filter(sender=user, status="A")
    if sInvitations:
        for i in sInvitations:
            friends.append(i.receiver)

    rInvitations = Invitation.objects.filter(receiver=user, status="A")
    if rInvitations:
        for j in rInvitations:
            friends.append(j.sender)

    pInvitations = Invitation.objects.filter(receiver=user, status="P")
    if pInvitations:
        for k in pInvitations:
            pending.append(k.sender)

    return (friends, pending)



class GetFriendsView(APIView):
    def post(self, request):
        """
        Method to get the friends of the logged user and his pending friends
        """
        user = getUserByToken(request)

        friends, pending = getFriendsOrPending(user)

        return Response({"friends": friends, "pending": pending})


class DiscoverPeopleView(APIView):
    def post(self, request):
        """
        Method to get the people who have the same interests as you in order to discover people
        """
        user = getUserByToken(request)

        friends, pending = getFriendsOrPending(user)

        discoverPeople = []
        interests = user.interest_set.all()

        # First, we obtain the people with the same interests
        for interest in interests:
            aux = UserProfile.objects.filter(interest_set__icontains=interest)
            for person in aux:
                if not person in discoverPeople:
                    discoverPeople.append(person)

        # After, we obtain the people without the same interests and append them at the end of the discover list
        allUsers = UserProfile.objects.all()
        allUsers.remove(discoverPeople)
        discoverPeople.append(allUsers)

        # Finally, we remove from the discover list the people who are our friends or pending friends
        discoverPeople.remove(friends)
        discoverPeople.remove(pending)

        return Response({"discoverPeople": discoverPeople})

class MyTripsList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = TripSerializer


    def get_queryset(self):
        return Trip.objects.filter(user__user=self.request.user).order_by('-startDate')

    
class AvailableTripsList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = TripSerializer

    
    def get_queryset(self):
        today = datetime.today()
        return Trip.objects.filter(
            Q(status = True) &
            Q(startDate__gte=today) &
            Q(tripType='PUBLIC')).exclude(user__user=self.request.user).order_by('-startDate')



class AvailableTripsSearch(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = TripSerializer


    def get_queryset(self):
        today = datetime.today()
        return Trip.objects.filter(
            Q(status = True) &
            Q(startDate__gte=today) &
            Q(tripType='PUBLIC')).exclude(user__user=self.request.user).order_by('-startDate')


    queryset = get_queryset
    serializer_class = TripSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description')



class ListCities(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,
                              SessionAuthentication)

    def get(self, request):


        cities = City.objects.all()
        return Response(CitySerializer(cities, many=True).data)

class CreateTrip(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,
                              SessionAuthentication)

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