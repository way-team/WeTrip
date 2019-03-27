from TravelMateServer.API.serializers import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import UserProfile, Invitation
from django.contrib.auth.models import User
from rest_framework import authentication, generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


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
    def get(self, request):
        """
        Method to get the friends of the logged user and his pending friends 
        """
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        user = tk.user

        try:
            friends = Invitation.objects.filter(Q(sender = user) | Q(receiver=user) , status="A")
            pendingFriends = Invitation.objects.filter(receiver=user , status="P")
        except:
            friends = []
            pendingFriends = []
        
        return Response({"friends": friends, "pendingFriends": pendingFriends})