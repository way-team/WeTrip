from TravelMateServer.API.serializers import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import UserProfile, Rate
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

class RateUser(APIView):

    def post(self, request):

        # key = request.data.get('token', '')
        # tk = get_object_or_404(Token, key=key)
        # user = tk.user

        #username = request.user.username
        username= request.data.get('username','')
        voter = User.objects.get(username="fran").userprofile

        votedUsername = request.data.get('voted', '')
        voted = User.objects.get(username=votedUsername).userprofile

        value = request.data.get('value', '')

        rate = Rate.objects.filter(voted=voted, voter=voter).first()
        if(rate==None):
            rate = Rate(voted=voted, voter=voter, value=value)
            rate.save()
        else:
            rate.value = value
            rate.save()

        def refreshUserAverageRating(user):
            userRatings = Rate.objects.filter(voted=user)
            sumRatings = 0
            for r in userRatings:
                sumRatings += r.value
            avgUserRating = sumRatings/userRatings.count()
            user.avarageRate = avgUserRating
            user.save()

        refreshUserAverageRating(voted)
        userProfile = UserProfile.objects.get(user=voted)

        return Response(UserProfileSerializer(voted, many=False).data)


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
