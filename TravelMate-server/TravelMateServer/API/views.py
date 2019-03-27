from TravelMateServer.API.serializers import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import UserProfile, Invitation
from django.contrib.auth.models import User
from rest_framework import authentication, generics
from rest_framework.permissions import IsAuthenticated


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
    authentication_classes = (authentication.TokenAuthentication,
                              authentication.SessionAuthentication)

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
