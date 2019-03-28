from TravelMateServer.API.serializers import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import UserProfile, City, Invitation
from django.contrib.auth.models import User
from rest_framework import authentication, generics
from rest_framework.permissions import IsAuthenticated


def get_user_by_token(request):
    key = request.data.get('token', '')
    tk = get_object_or_404(Token, key=key)
    user = tk.user
    user_profile = UserProfile.objects.get(user=user)

    return user_profile


class GetUserView(APIView):
    def post(self, request):
        user_profile = get_user_by_token(request)

        return Response(UserProfileSerializer(user_profile, many=False).data)


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
        trip = Trip(
            user=user,
            title=title,
            description=description,
            startDate=startDate,
            endDate=endDate,
            tripType=tripType,
            image=image)
        trip.save()

        #GET CITY AND ADD TRIP
        city = City.objects.get(pk=cityId)
        city.trips.add(trip)

        return Response(TripSerializer(trip, many=False).data)


def get_friends_or_pending(user):
    """
    Method to get the list of an user's friends or pending friends
    """
    friends = []
    pending = []

    sended_invitations = Invitation.objects.filter(sender=user, status="A")
    if sended_invitations:
        for i in sended_invitations:
            friends.append(i.receiver)

    received_invitations = Invitation.objects.filter(receiver=user, status="A")
    if received_invitations:
        for j in received_invitations:
            friends.append(j.sender)

    pending_invitations = Invitation.objects.filter(receiver=user, status="P")
    if pending_invitations:
        for k in pending_invitations:
            pending.append(k.sender)

    return (friends, pending)


class GetFriendsView(APIView):
    """
    Method to get the friends of the logged user
    """
    def post(self, request):
        """
        POST method
        """
        user = get_user_by_token(request)

        friends, pending = get_friends_or_pending(user)

        return Response(UserProfileSerializer(friends, many=True).data)


class GetPendingView(APIView):
    """
    Method to get the pending friends of the logged user
    """
    def post(self, request):
        """
        POST method
        """
        user = get_user_by_token(request)

        friends, pending = get_friends_or_pending(user)

        return Response(UserProfileSerializer(pending, many=True).data)


class DiscoverPeopleView(APIView):
    """
     Method to get the people who have the same interests as you in order to discover people
    """
    def post(self, request):
        """
        POST method
        """
        user = get_user_by_token(request)

        friends, pending = get_friends_or_pending(user)

        discover_people = []
        interests = user.interest_set.all()

        # First, we obtain the people with the same interests
        for interest in interests:
            aux = UserProfile.objects.filter(interest_set__icontains=interest)
            for person in aux:
                if not person in discover_people:
                    discover_people.append(person)

        # After, we obtain the people without the same interests
        # and append them at the end of the discover list
        all_users = UserProfile.objects.all()
        all_users.remove(discover_people)
        discover_people.append(all_users)

        # Finally, we remove from the discover list the people
        # who are our friends or pending friends
        discover_people.remove(friends)
        discover_people.remove(pending)

        return Response(UserProfileSerializer(discover_people, many=True).data)
