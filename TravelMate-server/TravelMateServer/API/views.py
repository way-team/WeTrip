from TravelMateServer.API.serializers import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import UserProfile, Invitation
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
        

class GetFriendsView(APIView):
    def post(self, request):
        """
        Method to get the friends of the logged user and his pending friends 
        """
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        user = tk.user

        friends = []
        pending = []

        try:
            sInvitations = Invitation.objects.filter(sender=user, status="A")
            rInvitations = Invitation.objects.filter(receiver=user, status="A")
            pInvitations = Invitation.objects.filter(receiver=user, status="P")
            
            for i in sInvitations:
                friends.append(i.receiver)
            for j in rInvitations:
                friends.append(j.sender)
            for k in pInvitations:
                pending.append(k.sender)

        except:
            friends = []
            pending = []

        return Response({"friends": friends, "pending": pending})


class DiscoverPeopleView(APIView):
    def post(self, request):
        """
        Method to get the people who have the same interests as you in order to discover people
        """
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        user = tk.user

        discoverPeople = []
        interests = user.interest_set.all()

        for interest in interests:
            aux = UserProfile.objects.filter(interest_set__icontains=interest)
            for person in aux:
                if not person in discoverPeople:
                    discoverPeople.append(person)

        return Response({"discoverPeople": discoverPeople})
