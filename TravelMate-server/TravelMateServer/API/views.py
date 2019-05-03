from TravelMateServer.API.serializers import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import FileResponse, HttpResponse
from rest_framework import generics, filters
from .models import UserProfile, Trip, Invitation, City, Rate, Application, Language, Interest
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q, Count, StdDev, Avg, Sum, Case, When, IntegerField, Value
from django.utils.datastructures import MultiValueDictKeyError
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from collections import namedtuple
from django.contrib.auth.hashers import make_password
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from string import Template
import smtplib
import re
import os
import json
import time
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from functools import partial
from reportlab.lib.enums import TA_CENTER


def get_user_by_token(request):
    key = request.data.get('token', '')
    tk = get_object_or_404(Token, key=key)
    user = tk.user
    user_profile = UserProfile.objects.get(user=user)
    
    # Sets user to no Premium if it's been 1 year since the user paid
    if user_profile.isPremium:
        today = datetime.today().date()
        datePremium = user_profile.datePremium
        if today > datePremium:
            user_profile.isPremium = False
            user_profile.save()

    return user_profile


class GetUserView(APIView):
    def post(self, request):
        user_profile = get_user_by_token(request)

        return Response(UserProfileSerializer(user_profile, many=False).data)


class GetUserByIdView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        user_id = request.data.get('user_id', '')
        user_profile = UserProfile.objects.get(pk=user_id)

        return Response(UserProfileSerializer(user_profile, many=False).data)


def refreshUserAverageRating(votedUserProfile):
    userRatings = Rate.objects.filter(voted=votedUserProfile)
    sumRatings = 0
    numRatings = 0
    for r in userRatings:
        sumRatings += r.value
        numRatings = numRatings + 1
    avgUserRating = sumRatings / numRatings
    votedUserProfile.avarageRate = avgUserRating
    votedUserProfile.numRate = numRatings
    votedUserProfile.save()


class RateUser(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request):
        userId = request.data.get('userId', '')
        user = User.objects.get(id=userId).userProfile
        refreshUserAverageRating(user)
        avgRating = user.avarageRate

        return Response(UserProfileSerializer(user, many=False).data)

    def post(self, request):
        """
        POST method
        """

        #Comment the following line and remove the comment from one after that to test with Postman
        username = request.user.username
        #username = request.data.get('username', '')
        voter0 = User.objects.get(username=username)
        voter = UserProfile.objects.get(user=voter0)

        votedusername = request.data.get('voted', '')
        voted0 = User.objects.get(username=votedusername)
        voteduser = UserProfile.objects.get(user=voted0)

        if voter.status == "D" :
            raise ValueError("Deleted users are not allowed to rate other users")
        elif voteduser.status == "D" :
            raise ValueError("You cannot rate a deleted user")
        else:
            value = request.data.get('rating', '0')

            areFriends = False
            friends, pending, rejected = get_friends(voter, False)
            for f in friends:
                if f == voteduser:
                    areFriends = True
                    break

            oldRating = Rate.objects.filter(voter=voter, voted=voteduser).first()
            if areFriends:
                actualrating = int(voteduser.avarageRate)
                numTimes = int(voteduser.numRate)
                new = int(value)

                if oldRating:
                    oldRating.delete()
                    old = int(oldRating.value)
                    voteduser.avarageRate = int(
                        (actualrating * numTimes + new - old) / (numTimes))

                else:
                    voteduser.avarageRate = int(
                        (actualrating * numTimes + new) / (numTimes + 1))
                    voteduser.numRate = numTimes + 1

                rate = Rate(voter=voter, voted=voteduser, value=value)
                voteduser.save()
                rate.save()
            else:
                raise ValueError("You can not rate this user")

        return Response(UserProfileSerializer(voteduser, many=False).data)


class UserList(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request, *args, **kwargs):
        """
        Get the user by his username
        """
        username = kwargs.get('username')
        userProfile = User.objects.get(username=username).userprofile
        return Response(UserProfileSerializer(userProfile, many=False).data)


def get_friends(user, discover):
    """
    Method to get the list of an user's friends or pending friends
    """
    friends = []
    pending = []
    rejected = []

    sended_accepted = Invitation.objects.filter(sender=user, status="A")
    if sended_accepted:
        for i in sended_accepted:
            if i.receiver.status=='A':
                friends.append(i.receiver)

    received_accepted = Invitation.objects.filter(receiver=user, status="A")
    if received_accepted:
        for j in received_accepted:
            if j.sender.status=='A':
                friends.append(j.sender)

    sended_rejected = Invitation.objects.filter(sender=user, status="R")
    if sended_rejected:
        for i in sended_rejected:
            if i.receiver.status=='A':
                rejected.append(i.receiver)

    received_rejected = Invitation.objects.filter(receiver=user, status="R")
    if received_rejected:
        for j in received_rejected:
            if j.sender.status=='A':
                rejected.append(j.sender)

    received_pending = Invitation.objects.filter(receiver=user, status="P")
    if received_pending:
        for i in received_pending:
            if i.sender.status=='A':
                pending.append(i.sender)

    if discover:
        sended_pending = Invitation.objects.filter(sender=user, status="P")
        if sended_pending:
            for j in sended_pending:
                pending.append(j.receiver)


    return (friends, pending, rejected)

def get_deleted_users():
    """
    Method to get the list of all deleted users
    """
    users = []

    users_deleted = UserProfile.objects.filter(status="D")
    for i in users_deleted:
        users.append(i)

    return users

class GetFriendsView(APIView):
    """
    Method to get the friends of the logged user
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        user = get_user_by_token(request)

        friends, pending, rejected = get_friends(user, False)

        return Response(UserProfileSerializer(friends, many=True).data)


class GetPendingView(APIView):
    """
    Method to get the pending friends of the logged user
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        user = get_user_by_token(request)

        friends, pending, rejected = get_friends(user, False)

        return Response(UserProfileSerializer(pending, many=True).data)

class GetPendingInvitationsView(APIView):
    """
    Method to get the user's invitations not accepted
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        pendingI=[]

        user = get_user_by_token(request)

        pendingInvitations = get_pendingInvitations(user, False)
        if pendingInvitations:
            for i in pendingInvitations:
                if i.receiver.status=='A':
                    pendingI.append(i.receiver)

        return Response(UserProfileSerializer(pendingI, many=True).data)



def get_pendingInvitations(user, discover):
    """
    Method to get the list of an user's invitations not accepted
    """

    pendingInvitations = []

    pendingInvitations = Invitation.objects.filter(sender=user, status="P")

    return pendingInvitations


class SendInvitation(APIView):
    """
    Method to send a friend invitation to other user
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        sender = get_user_by_token(request)

        receivername = request.data.get("username", "")
        receiver = User.objects.get(username=receivername).userprofile

        allinvitations = Invitation.objects.all()

        control = None

        for invitation in allinvitations:
            if invitation.sender == receiver and invitation.receiver == sender and invitation.status == "P":
                control = "A"
                break
            elif invitation.sender == sender and invitation.receiver == receiver and invitation.status == "P":
                control = "B"
                break
            elif invitation.sender == receiver and invitation.receiver == sender and invitation.status == "R":
                control = "C"
                break
            elif invitation.sender == sender and invitation.receiver == receiver and invitation.status == "R":
                control = "D"
                break
            elif invitation.sender == receiver and invitation.receiver == sender and invitation.status == "A":
                control = "E"
                break
            elif invitation.sender == sender and invitation.receiver == receiver and invitation.status == "A":
                control = "F"
                break

        if sender == receiver:
            control = "G"
            
        if sender.status == "D":
            control = "H"

        if receiver.status == "D":
            control = "I"

        if control == "A":
            raise ValueError(
                "This person has sent you a friend request before")
        elif control == "B":
            raise ValueError(
                "You already sent a friend request to this person before")
        elif control == "C":
            raise ValueError("You already rejected this person")
        elif control == "D":
            raise ValueError("This person has rejected you")
        elif control == "E":
            raise ValueError("You are already friends")
        elif control == "F":
            raise ValueError("You are already friends")
        elif control == "G":
            raise ValueError("You can't be your own friend")
        elif control == "H":
            raise ValueError("A deleted user cannot send an invitation")
        elif control == "I":
            raise ValueError("You cannot send an invitation to a deleted user")
        elif control == None:
            newinvitation = Invitation(
                sender=sender, receiver=receiver, status="P")
            newinvitation.save()

        return Response(InvitationSerializer(newinvitation, many=False).data)


class AcceptFriend(APIView):
    """
    Method to accept an invitation to be a friend of the logged user
    """

    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        user = get_user_by_token(request)

        if user.status == "D":
            raise ValueError("Deleted users can't accept friend invitations")

        sendername = request.data.get("sendername", "")
        sender = User.objects.get(username=sendername).userprofile

        try:
            invitation = Invitation.objects.filter(
                sender=sender, status="P").get(receiver=user)
        except Invitation.DoesNotExist:
            invitation = None

        if invitation is not None:
            invitation.status = "A"
            invitation.save()
        else:
            raise ValueError(
                "There is no pending invitation for that two users")

        return Response(InvitationSerializer(invitation, many=False).data)


class RejectFriend(APIView):
    """
    Method to decline an invitation to be a friend of the logged user
    """

    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        user = get_user_by_token(request)

        if user.status == "D":
            raise ValueError("Deleted users can't reject friend invitations")

        sendername = request.data.get("sendername", "")
        sender = User.objects.get(username=sendername).userprofile

        try:
            invitation = Invitation.objects.filter(
                sender=sender, status="P").get(receiver=user)
        except Invitation.DoesNotExist:
            invitation = None

        if invitation is not None:
            invitation.status = "R"
            invitation.save()
        else:
            raise ValueError(
                "There is no pending invitation for that two users")

        return Response(InvitationSerializer(invitation, many=False).data)


class RemoveFriend(APIView):
    """
    Method to remove a friend of the logged user
    """

    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        user = get_user_by_token(request)

        sendername = request.data.get("sendername", "")
        sender = User.objects.get(username=sendername).userprofile

        try:
            invitation = Invitation.objects.get(Q(sender=sender, receiver=user, status="A") | Q(sender=user, receiver=sender, status="A"))
        except Invitation.DoesNotExist:
            invitation = None

        if invitation is not None:
            invitation.status = "R"
            invitation.save()
        else:
            raise ValueError("No relation between these two users")

        return Response(InvitationSerializer(invitation, many=False).data)

class DiscoverPeopleView(APIView):
    """
    Method to get the people who have the same interests as you in order to discover people
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        user = get_user_by_token(request)
        friends, pending, rejected = get_friends(user, True)
        limit = int(request.data.get("limit",""))
        offset = int(request.data.get("offset",""))
        discover_people = []
        interests = user.interests.all()
        # First, we obtain the people with the same interests
        ranking = []
        for interest in interests:
            usersWithInterest = interest.users.all()
            for person in usersWithInterest:
                ranking.append(person)

        
        #Now, we get friends of the user's friends
        for friend in friends:
            friendsOfFriend, pendingOfFriend, rejectedOfFriend = get_friends(friend, False)

            for f in friendsOfFriend:
                ranking.append(f)
        

        #We get users who are going (or went) on the same trips as the user
        userApps = Application.objects.filter(applicant= user, status='A')
        for a in userApps:
            applications = Application.objects.filter(trip=a.trip, status="A")


            for appOfFriend in applications:
                ranking.append(appOfFriend.applicant)

        #Now the list is sorted by the number of times a user appears in it
        import collections
        ranking = collections.Counter(ranking).most_common()
        discover_people = [i[0] for i in ranking]

        
        #This line gets rid of duplicated users in the list
        discover_people = list(dict.fromkeys(discover_people))
        

        '''all_users = list(UserProfile.objects.all())
        for person in discover_people:
            all_users.remove(person)
        for person in all_users:
            discover_people.add(person)'''

        # Finally, we remove from the discover list the people
        # who are our friends or pending friends
        for person in friends:
            if(person in discover_people):
                discover_people.remove(person)
        for person in pending:
            if(person in discover_people):
                discover_people.remove(person)
        for person in rejected:
            if(person in discover_people):
                discover_people.remove(person)
        # who are the deleted users and remove them
        deleted_users = get_deleted_users()
        for person in deleted_users:
            if(person in discover_people):
                discover_people.remove(person)


        if(user in discover_people):
                discover_people.remove(user)

        return Response(UserProfileSerializer(discover_people[limit:limit+offset], many=True).data)


class MyTripsList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = TripSerializer

    def get_queryset(self):
        return Trip.objects.filter(
            user__user=self.request.user).order_by('-startDate')


def get_available_trips(user_profile):

    today = datetime.today()
    
    myRejectedApplications = Application.objects.filter(applicant_id = user_profile.id, status='R')
    myRejectedAppTripsIds = Trip.objects.filter(applications__in=myRejectedApplications).values_list('id', flat=True)
    premiumUsers = UserProfile.objects.filter(isPremium=1).values_list('id', flat=True)

    return Trip.objects.annotate(isPremiumUser=Case(When(user_id__in=premiumUsers, then=Value(1)),default=Value(0),output_field=IntegerField())).filter(
        Q(status=True) & Q(startDate__gte=today) & Q(
            tripType='PUBLIC')).exclude(
                user=user_profile).exclude(id__in=myRejectedAppTripsIds).order_by('-isPremiumUser')


def get_available_trips_for_apply(user_profile):

    today = datetime.today()
    
    myApplications = Application.objects.filter(applicant_id = user_profile.id)
    myAppTripsIds = Trip.objects.filter(applications__in=myApplications).values_list('id', flat=True)
    premiumUsers = UserProfile.objects.filter(isPremium=1).values_list('id', flat=True)

    return Trip.objects.annotate(isPremiumUser=Case(When(user_id__in=premiumUsers, then=Value(1)),default=Value(0),output_field=IntegerField())).filter(
        Q(status=True) & Q(startDate__gte=today) & Q(
            tripType='PUBLIC')).exclude(
                user=user_profile).exclude(id__in=myAppTripsIds).order_by('-isPremiumUser')



class AvailableTripsList(generics.ListAPIView):
    ''' Gets trips available (Application not rejected) '''
    
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = TripSerializer

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)

        return get_available_trips(user_profile)


class AvailableTripsSearch(generics.ListAPIView):
    ''' Search trips available (Application not rejected) '''

    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = TripSerializer

    def get_queryset(self):

        user_profile = UserProfile.objects.get(user=self.request.user)

        return get_available_trips(user_profile)

    queryset = get_queryset
    serializer_class = TripSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('title', 'description')


class ListCities(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request):

        cities = City.objects.all()
        return Response(CitySerializer(cities, many=True).data)


class ListLanguages(APIView):
    def get(self, request):

        languages = Language.objects.all()
        return Response(LanguageSerializer(languages, many=True).data)


class ListInterest(APIView):
    def get(self, request):

        interests = Interest.objects.all()
        return Response(InterestNameSerializer(interests, many=True).data)


class CreateTrip(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):

        data = request.data
        #GET TRIP DATA
        #Comment the following line and remove the comment from one after that to test with Postman
        username = request.user.username
        #username= request.data.get('username','')
        user = User.objects.get(username=username).userprofile
        title = request.data.get('title', '')
        description = request.data.get('description', '')
        price = request.data.get('price', '0')
        startDate = request.data.get('start_date', '')
        endDate = request.data.get('end_date', '')
        tripType = request.data.get('trip_type', '')

        if user.status == "D":
            raise ValueError("Deleted users can't create trips")

        if data.get('start_date') > data.get('end_date'):
            raise ValueError("The start date must be before the end date")

        if not (tripType == 'PUBLIC' or tripType == 'PRIVATE'):
            raise ValueError("Invalid trip type")

        if int(price) < 0:
            raise ValueError("Price can't be negative")


        #GET CITY DATA
        cities = json.loads(request.data.get('cities'))
        
        
        
        if(len(cities) == 1):
            city = City.objects.get(pk=cities[0])
            image_name = city.country.name + '.jpg'
        else:
            first_country = City.objects.get(pk=cities[0]).country
            world = False
            for i in cities:
                country = City.objects.get(pk=i).country
                if(country != first_country):
                    world = True
                    break

            if(world):
                image_name = 'World.jpg'
            else:
                image_name = first_country.name + '.jpg'

            
        
        

        try:
            userImage = request.data['file']
            trip = Trip(
                user=user,
                title=title,
                description=description,
                price=price,
                startDate=startDate,
                endDate=endDate,
                tripType=tripType,
                image=image_name,
                userImage=userImage)

            trip.save()

        except MultiValueDictKeyError:
            trip = Trip(
                user=user,
                title=title,
                description=description,
                price=price,
                startDate=startDate,
                endDate=endDate,
                tripType=tripType,
                image=image_name)

            trip.save()
        finally:
            #GET CITY AND ADD TRIP
            for i in cities:
                city = City.objects.get(pk=i)
                city.trips.add(trip)

            return Response(TripSerializer(trip, many=False).data)


FullTrip = namedtuple('FullTrip', ('trip', 'applicationsList', 'pendingsList', 'rejectedList'))


class GetTripView(APIView):
    """
    Method to get a trip by its ID
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request, *args, **kwargs):
        """
        GET method
        """
        trip_id = kwargs.get("trip_id", "")
        try:
            trip = Trip.objects.get(pk=trip_id)

            if trip.status == False:
                raise ValueError("This trip is deleted")

            applications = Application.objects.filter(trip=trip, status="A")
            pendings = Application.objects.filter(trip=trip, status="P")
            rejected = Application.objects.filter(trip=trip, status="R")

            full_trip = FullTrip(
                trip=trip,
                applicationsList=applications,
                pendingsList=pendings,
                rejectedList=rejected,
            )
            return Response(FullTripSerializer(full_trip, many=False).data)
        except Trip.DoesNotExist:
            raise ValueError("The trip does not exist")


class EditTripView(APIView):
    """
    Method to edit a trip by its ID
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        data = request.data
        
        trip = Trip.objects.get(pk=request.data["tripId"])
        for i in trip.cities.all():
            i.trips.remove(trip)
        

        if trip.status == False:
            raise ValueError("This trip is deleted")

        if trip.tripType == "PUBLIC": 
            raise ValueError("This trip is public, so it can't be edited ")

        stored_creator = trip.user
        user = get_user_by_token(request)
        if stored_creator != user:
            raise ValueError("You are not the creator of this trip")

    
        if data.get('startDate') > data.get('endDate'):
            raise ValueError("The start date must be before the end date")

        if data.get('file'):
            trip.userImage = data.get('file')
    
        cities = json.loads(data.get('cities'))

        if(len(cities) == 1):
            city = City.objects.get(pk=cities[0])
            image_name = city.country.name + '.jpg'
        else:
            first_country = City.objects.get(pk=cities[0]).country
            world = False
            for i in cities:
                country = City.objects.get(pk=i).country
                if(country != first_country):
                    world = True
                    break

            if(world):
                image_name = 'World.jpg'
            else:
                image_name = first_country.name + '.jpg'

        title = data.get('title')
        description = data.get('description')
        price = data.get('price')
        startDate = data.get('startDate')
        endDate = data.get('endDate')
        tripType = data.get('tripType')

        if not (tripType == 'PUBLIC' or tripType == 'PRIVATE'):
            raise ValueError("Invalid trip type")

        if int(price) < 0:
            raise ValueError("Price can't be negative")
       

        trip.title = title
        trip.description = description
        trip.price = price
        trip.startDate = startDate
        trip.endDate = endDate
        trip.tripType = tripType
        trip.image = image_name
        try:
            trip.save()
        except:
            raise ValueError("Error saving trip")
        try:
            for i in cities:
                city = City.objects.get(pk=i)
                city.trips.add(trip)
        except City.DoesNotExist:
            raise ValueError("The city does not exist")

        return JsonResponse({'message':'Edit success'}, status=201)
        return JsonResponse({'error':'Error editing'}, status=400)


class DashboardData(APIView):
    """
    Method to apply to a trip specified by its ID
    """
    permission_classes = (IsAdminUser, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        stats = {}
        numberOfTrips = Trip.objects.all().count()
        stats['numberOfTrips'] = numberOfTrips
        stats['numberOfTripsJanuary'] = Trip.objects.filter(
            Q(startDate__month='01')).count()
        stats['numberOfTripsFebruary'] = Trip.objects.filter(
            Q(startDate__month='02')).count()
        stats['numberOfTripsMarch'] = Trip.objects.filter(
            Q(startDate__month='03')).count()
        stats['numberOfTripsApril'] = Trip.objects.filter(
            Q(startDate__month='04')).count()
        stats['numberOfTripsMay'] = Trip.objects.filter(
            Q(startDate__month='05')).count()
        stats['numberOfTripsJune'] = Trip.objects.filter(
            Q(startDate__month='06')).count()
        stats['numberOfTripsJuly'] = Trip.objects.filter(
            Q(startDate__month='07')).count()
        stats['numberOfTripsAugust'] = Trip.objects.filter(
            Q(startDate__month='08')).count()
        stats['numberOfTripsSeptember'] = Trip.objects.filter(
            Q(startDate__month='09')).count()
        stats['numberOfTripsOctober'] = Trip.objects.filter(
            Q(startDate__month='10')).count()
        stats['numberOfTripsNovember'] = Trip.objects.filter(
            Q(startDate__month='11')).count()
        stats['numberOfTripsDecember'] = Trip.objects.filter(
            Q(startDate__month='12')).count()

        numberOfPublicTrips = Trip.objects.filter(tripType='PUBLIC').count()
        numberOfPrivateTrips = Trip.objects.filter(tripType='PRIVATE').count()
        stats['numberOfPublicTrips'] = numberOfPublicTrips
        stats['numberOfPrivateTrips'] = numberOfPrivateTrips
        if (numberOfPublicTrips != 0):
            stats[
                'ratioOfPrivateTrips'] = numberOfPrivateTrips / numberOfPublicTrips
        else:
            stats['ratioOfPrivateTrips'] = 0
        stats['percentagePrivateTrips'] = numberOfPrivateTrips / numberOfTrips
        stats['percentagePublicTrips'] = numberOfPublicTrips / numberOfTrips

        numberOfUsers = UserProfile.objects.all().count()
        stats['numberOfUsers'] = numberOfUsers

        stats['numberMen'] = UserProfile.objects.filter(gender='M').count()
        stats['numberWomen'] = UserProfile.objects.filter(gender='F').count()
        stats['numberNonBinary'] = UserProfile.objects.filter(
            gender='N').count()

        stats['percentageMen'] = UserProfile.objects.filter(
            gender='M').count() / numberOfUsers
        stats['percentageWomen'] = UserProfile.objects.filter(
            gender='F').count() / numberOfUsers
        stats['percentageNonBinary'] = UserProfile.objects.filter(
            gender='N').count() / numberOfUsers

        numberOfPremiumUsers = UserProfile.objects.filter(
            isPremium=True).count()
        numberOfNonPremiumUsers = UserProfile.objects.filter(
            isPremium=False).count()
        stats['numberOfPremiumUsers'] = numberOfPremiumUsers
        stats['numberOfNonPremiumUsers'] = numberOfNonPremiumUsers
        stats['percentagePremiumUsers'] = numberOfPremiumUsers / numberOfUsers
        stats[
            'percentageNonPremiumUsers'] = numberOfNonPremiumUsers / numberOfUsers

        activeUsers = UserProfile.objects.filter(status='A').count()
        deletedUsers = UserProfile.objects.filter(status='D').count()

        if (deletedUsers != 0):
            stats['activeUsersRatio'] = activeUsers / deletedUsers
        else:
            stats['activeUsersRatio'] = 0

        stats['numberOfActiveUsers'] = activeUsers
        stats['numberOfDeletedUsers'] = deletedUsers
        stats['percentageActiveUsers'] = activeUsers / numberOfUsers
        stats['percentageDeletedUsers'] = deletedUsers / numberOfUsers

        if (numberOfNonPremiumUsers != 0):
            stats[
                'premiumUsersRatio'] = numberOfPremiumUsers / numberOfNonPremiumUsers
        else:
            stats['premiumUsersRatio'] = 0

        stats['avgTripsPerUser'] = numberOfTrips / numberOfUsers

        numberOfApps = Application.objects.all().count()
        stats['avgAppsPerTrip'] = numberOfApps / numberOfTrips

        numberOfLanguages = Language.objects.all().count()
        stats['avgLanguagesPerUser'] = numberOfLanguages / numberOfUsers
        #stats['stDevLanguagesPerUser']=

        stats['avgRatingPerUser'] = UserProfile.objects.aggregate(
            Avg('avarageRate'))['avarageRate__avg']
        #stats['stDevRatingPerUser']=
        stats['top5AppsTrips'] = TripSerializer(
            Trip.objects.annotate(
                apps=Count('applications')).order_by('-apps')[:5],
            many=True).data
        stats['top5NumberOfCitiesTrips'] = TripSerializer(
            Trip.objects.annotate(
                cities_count=Count('cities')).order_by('-cities_count')[:5],
            many=True).data
        stats['top5NumberOfTripsCities'] = CityReducedSerializer(
            City.objects.annotate(
                trips_count=Count('trips')).order_by('-trips_count')[:5],
            many=True).data
        stats['top5MostCommonInterests'] = InterestReducedSerializer(
            Interest.objects.annotate(
                users_count=Count('users')).order_by('-users_count')[:5],
            many=True).data

        return JsonResponse(stats)


class ApplyTripView(APIView):
    """
    Method to apply to a trip specified by its ID
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        user = get_user_by_token(request)

        if user.status == "D":
            raise ValueError("Deleted users can't apply for trips")

        trip_id = request.data.get("trip_id", "")
        trip = Trip.objects.get(pk=trip_id)

        available_trips_list = get_available_trips_for_apply(user)

        if trip not in available_trips_list:
            raise ValueError("You can't apply for this trip.")
        else:
            application = Application(applicant=user, trip=trip, status="P")
            application.save()
            
        return Response(TripSerializer(trip, many=False).data)


class AcceptApplicationView(APIView):
    """
    Method to accept an application to a trip specified by their IDs
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        user = get_user_by_token(request)

        if user.status == "D":
            raise ValueError("Deleted users can't accept applications")

        aplication_id = request.data.get("application_id", "")

        try:
            application = Application.objects.get(pk=aplication_id)
            creator = application.trip.user
            if creator != user:
                raise ValueError(
                    "You are not the creator of the application's trip")
            if application.status != "P":
                raise ValueError(
                    "The application has just accepted or rejected")
            application.status = "A"
            application.save()
            return Response(TripSerializer(application.trip, many=False).data)
        except Application.DoesNotExist:
            raise ValueError("The application does not exist")


class RejectApplicationView(APIView):
    """
    Method to reject an application to a trip specified by their IDs
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        user = get_user_by_token(request)

        if user.status == "D":
            raise ValueError("Deleted users can't reject applications")

        aplication_id = request.data.get("application_id", "")

        try:
            application = Application.objects.get(pk=aplication_id)
            creator = application.trip.user
            if creator != user:
                raise ValueError(
                    "You are not the creator of the application's trip")
            if application.status != "P":
                raise ValueError(
                    "The application has just accepted or rejected")
            application.status = "R"
            application.save()
            return Response(TripSerializer(application.trip, many=False).data)
        except Application.DoesNotExist:
            raise ValueError("The application does not exist")


class SetUserToPremium(APIView):
    """
    Makes a user Premium
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        usernamepaid = request.user.username
        userpaid = User.objects.get(username=usernamepaid)
        userprofilepaid = UserProfile.objects.get(user=userpaid)

        if userprofilepaid.status == "D":
            raise ValueError("Deleted users can't be Premium")
        
        else:

            if not userprofilepaid.isPremium:
                userprofilepaid.isPremium = True
                userprofilepaid.datePremium = datetime.today().date() + relativedelta(years=1)
            else:
                userprofilepaid.datePremium += relativedelta(years=1)

            userprofilepaid.save()

        return Response(
            UserProfileSerializer(userprofilepaid, many=False).data)


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    if request.method == 'GET':
        messagesSend = Message.objects.filter(
            sender_id=sender, receiver_id=receiver)
        messagesReceives = Message.objects.filter(
            sender_id=receiver, receiver_id=sender)

        allmessages = messagesSend | messagesReceives
        messages = allmessages.order_by('timestamp')

        serializer = MessageSerializer(
            messages, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = request.POST
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class RegisterUser(APIView):
    def post(self, request):
        #username = request.user.username
        #password = make_password(request.user.password)
        username = request.data.get('username', '')
        password = make_password(request.data.get('password', ''))
        email = request.data.get('email', '')
        firstName = request.data.get('first_name', '')
        lastName = request.data.get('last_name', '')
        description = request.data.get('description', '')
        birthdate = request.data.get('birthdate', '')
        
        # To check if > 18 years old
        today = datetime.today()  
        birthdate_date = datetime.strptime(birthdate, '%Y-%m-%d')
        age = today.year - birthdate_date.year - ((today.month, today.day) < (birthdate_date.month, birthdate_date.day))
        if age < 18:
            return JsonResponse({'error':'Underage'}, status=500)


        gender = request.data.get('gender', '')

        if not (gender == "M" or gender == "W" or gender == "N"):
            return JsonResponse({'error':'Invalid gender'}, status=500)


    
        nationality = request.data.get('nationality', '')
        city = request.data.get('city', '')
        profesion = request.data.get('profesion', '')
        civilStatus = request.data.get('civilStatus', '')

        if not (civilStatus == "M" or civilStatus == "S" or civilStatus=="R" or civilStatus == "W" or civilStatus == "D"):
            return JsonResponse({'error':'Invalid civil status'}, status=500)

        status = 'A'


        languages = json.loads(request.data.get('languages'))
        interests = json.loads(request.data.get('interests'))

        user = User(username=username, password=password)
        user.save()
        try:
            photo = request.data['photo']
            discoverPhoto = request.data['discoverPhoto']

            userProfile = UserProfile(
                user=user,
                email=email,
                first_name=firstName,
                last_name=lastName,
                description=description,
                birthdate=birthdate,
                gender=gender,
                nationality=nationality,
                city=city,
                status=status,
                profesion=profesion,
                civilStatus=civilStatus,
                photo=photo,
                discoverPhoto=discoverPhoto)

            userProfile.save()
            for i in languages:
                lang = Language.objects.get(name=i)
                userProfile.languages.add(lang)
            for i in interests:
                inter = Interest.objects.get(name=i)
                inter.users.add(userProfile)
        except:

            try:
                photo = request.data['photo']

                userProfile = UserProfile(
                    user=user,
                    email=email,
                    first_name=firstName,
                    last_name=lastName,
                    description=description,
                    birthdate=birthdate,
                    gender=gender,
                    nationality=nationality,
                    city=city,
                    status=status,
                    profesion=profesion,
                    civilStatus=civilStatus,
                    photo=photo)

                userProfile.save()
                for i in languages:
                    lang = Language.objects.get(name=i)
                    userProfile.languages.add(lang)
                for i in interests:
                    inter = Interest.objects.get(name=i)
                    inter.users.add(userProfile)
            
            except:
                try:
                    discoverPhoto = request.data['discoverPhoto']

                    userProfile = UserProfile(
                        user=user,
                        email=email,
                        first_name=firstName,
                        last_name=lastName,
                        description=description,
                        birthdate=birthdate,
                        gender=gender,
                        nationality=nationality,
                        city=city,
                        status=status,
                        profesion=profesion,
                        civilStatus=civilStatus,
                        discoverPhoto=discoverPhoto)

                    userProfile.save()
                    for i in languages:
                        lang = Language.objects.get(name=i)
                        userProfile.languages.add(lang)
                    for i in interests:
                        inter = Interest.objects.get(name=i)
                        inter.users.add(userProfile)
                except:
                    userProfile = UserProfile(
                        user=user,
                        email=email,
                        first_name=firstName,
                        last_name=lastName,
                        description=description,
                        birthdate=birthdate,
                        gender=gender,
                        nationality=nationality,
                        city=city,
                        status=status,
                        profesion=profesion,
                        civilStatus=civilStatus)
                    userProfile.save()
                    for i in languages:
                        lang = Language.objects.get(name=i)
                        userProfile.languages.add(lang)
                    for i in interests:
                        inter = Interest.objects.get(name=i)
                        inter.users.add(userProfile)
            

        finally:
            return JsonResponse({'message':'Sign up performed successfuly'}, status=201)

class EditUser(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    
    def post(self, request):
       
        email = request.data.get('email', '')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        description = request.data.get('description', '')
        birthdate = request.data.get('birthdate', '')
        
        # To check if > 18 years old
        today = datetime.today()  
        birthdate_date = datetime.strptime(birthdate, '%Y-%m-%d')
        age = today.year - birthdate_date.year - ((today.month, today.day) < (birthdate_date.month, birthdate_date.day))
        if age < 18:
            return JsonResponse({'error':'Underage'}, status=500)

        gender = request.data.get('gender', '')

        if not (gender == "M" or gender == "W" or gender == "N"):
            return JsonResponse({'error':'Invalid gender'}, status=500)


        nationality = request.data.get('nationality', '')
        city = request.data.get('city', '')
        profesion = request.data.get('profesion', '')
        civilStatus = request.data.get('civilStatus', '')

        if not (civilStatus == "M" or civilStatus == "S" or civilStatus=="R" or civilStatus == "W" or civilStatus == "D"):
            return JsonResponse({'error':'Invalid civil status'}, status=500)

        status = 'A'
        
        languages = json.loads(request.data.get('languages'))
        interests = json.loads(request.data.get('interests'))

        user = get_user_by_token(request)

        if user.status == "D":
            return JsonResponse({'error':'Deleted user'}, status=500)

        for i in user.languages.all():
            user.languages.remove(i)
        for i in user.interests.all():
            user.interests.remove(i)

        try:
            photo = request.data['photo']
            discoverPhoto = request.data['discoverPhoto']

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.description = description
            user.birthdate = birthdate
            user.gender = gender
            user.nationality = nationality
            user.city = city
            user.status = status
            user.profesion = profesion
            user.civilStatus = civilStatus
            user.photo = photo
            user.discoverPhoto = discoverPhoto

            user.save()
            for i in languages:
                lang = Language.objects.get(name=i)
                user.languages.add(lang)
            for i in interests:
                inter = Interest.objects.get(name=i)
                inter.users.add(user)
        except:

            try:
                photo = request.data['photo']

                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.description = description
                user.birthdate = birthdate
                user.gender = gender
                user.nationality = nationality
                user.city = city
                user.status = status
                user.profesion = profesion
                user.civilStatus = civilStatus
                user.photo = photo

                user.save()
                for i in languages:
                    lang = Language.objects.get(name=i)
                    user.languages.add(lang)
                for i in interests:
                    inter = Interest.objects.get(name=i)
                    inter.users.add(user)
            
            except:
                try:
                    discoverPhoto = request.data['discoverPhoto']

                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.description = description
                    user.birthdate = birthdate
                    user.gender = gender
                    user.nationality = nationality
                    user.city = city
                    user.status = status
                    user.profesion = profesion
                    user.civilStatus = civilStatus
                    user.discoverPhoto = discoverPhoto

                    user.save()
                    for i in languages:
                        lang = Language.objects.get(name=i)
                        user.languages.add(lang)
                    for i in interests:
                        inter = Interest.objects.get(name=i)
                        inter.users.add(user)
                except:
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.description = description
                    user.birthdate = birthdate
                    user.gender = gender
                    user.nationality = nationality
                    user.city = city
                    user.status = status
                    user.profesion = profesion
                    user.civilStatus = civilStatus

                    
                    
                    user.save()
                    for i in languages:
                        lang = Language.objects.get(name=i)
                        user.languages.add(lang)
                    for i in interests:
                        inter = Interest.objects.get(name=i)
                        inter.users.add(user)
            

        finally:
            return JsonResponse({'message':'Edit performed successfuly'}, status=201)


class DeleteUser(APIView):
    """
    Change the user's status to deleted
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        user_id = request.data.get("user_id", "")
        user = User.objects.get(pk=user_id)
        userprofile = user.userprofile

        user.is_active = False
        user.save()

        userprofile.languages.clear()
        userprofile.email = "-"
        userprofile.first_name = "-"
        userprofile.last_name = "-"
        userprofile.description = "-"
        userprofile.city = "-"
        userprofile.nationality = "-"
        userprofile.photo = "user/profile/default.jpg"
        userprofile.discoverPhoto = "user/discover/d_default.jpg"
        userprofile.averageRate = 0
        userprofile.numRate = 0
        userprofile.isPremium = False
        userprofile.profesion = "-"
        userprofile.status = "D"
        userprofile.save()

        Application.objects.filter(applicant=userprofile).delete()
        Invitation.objects.filter(sender=userprofile).delete()
        Invitation.objects.filter(receiver=userprofile).delete()

        return Response(UserProfileSerializer(userprofile, many=False).data)


def send_mail(subject, body, email, attachment):
    """
    Send an email with an attachment
    """
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login("way.team.soft@gmail.com", "wayteam2019")

    msg = MIMEMultipart()

    msg['From'] = "way.team.soft@gmail.com"
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment != None:
        part = MIMEApplication(open(attachment, "rb").read())
        namePattern = re.compile(r"exported_data_.*")
        name = namePattern.search(attachment).group(0)
        part.add_header('Content-Disposition', 'attachment', filename=name)
        msg.attach(part)

    server.send_message(msg)
    del msg

    server.quit()


class ExportUserData(APIView):
    """
    Export the user's data as PDF and send it by email
    """
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def personal_table(self, user, userprofile, language):
        if language == "es":
            tableData = [["NOMBRE", userprofile.first_name]]
            tableData.append(["APELLIDOS", userprofile.last_name])
            tableData.append(["USERNAME", user.username])
            tableData.append(["DESCRIPCIÓN", userprofile.description])
            tableData.append(["GÉNERO", userprofile.gender])
            tableData.append(["CUMPLEAÑOS", userprofile.birthdate])
            tableData.append(["CIUDAD", userprofile.city])
            tableData.append(["NACIONALIDAD", userprofile.nationality])
            tableData.append(["URL DE FOTO", userprofile.photo])
            tableData.append(["URL DE FOTO DEL DISCOVER", userprofile.discoverPhoto])
            tableData.append(["VALORACIÓN MEDIA", userprofile.avarageRate])
            tableData.append(["NÚMERO DE VALORACIONES", userprofile.numRate])
            if userprofile.isPremium is True:
                tableData.append(["FECHA DE PREMIUM", userprofile.datePremium])

        else:
            tableData = [["NAME", userprofile.first_name]]
            tableData.append(["LAST NAME", userprofile.last_name])
            tableData.append(["USERNAME", user.username])
            tableData.append(["DESCRIPTION", userprofile.description])
            tableData.append(["GENDER", userprofile.gender])
            tableData.append(["BIRTHDATE", userprofile.birthdate])
            tableData.append(["CITY", userprofile.city])
            tableData.append(["NATIONALITY", userprofile.nationality])
            tableData.append(["PHOTO'S URL", userprofile.photo])
            tableData.append(["DISCOVER PHOTO'S URL", userprofile.discoverPhoto])
            tableData.append(["AVERAGE RATE", userprofile.avarageRate])
            tableData.append(["RATES NUMBER", userprofile.numRate])
            if userprofile.isPremium is True:
                tableData.append(["PREMIUM DATE", userprofile.datePremium])
       
        table = Table(data=tableData)
        table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                   ('INNERGRID', (0, 0), (0, 1), 0.5, colors.black),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                   ('FONTSIZE', (0, 0), (-1, -1), 10),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        return table

    def created_trips_table(self, trips, language):
        if language == "es":
            tableData = [["TÍTULO", "TIPO", "ESTADO"]]
            
        else:
            tableData = [["TITLE", "TYPE", "STATUS"]]

        for trip in trips:
            tableData.append([trip.title, trip.tripType, trip.status])
       
        table = Table(data=tableData)
        table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                   ('INNERGRID', (0, 0), (0, 1), 0.5, colors.black),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                   ('FONTSIZE', (0, 0), (-1, -1), 10),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        return table

    def invitations_table(self, sended, received, language):
        if language == "es":
            tableData = [["REMITENTE", "RECEPTOR", "ESTADO"]]
            
        else:
            tableData = [["SENDER", "RECEIVER", "STATUS"]]

        for sen in sended:
            tableData.append([sen.sender.get_full_name(), sen.receiver.first_name, sen.status])

        for rec in received:
            tableData.append([rec.sender.first_name, rec.receiver.get_full_name(), rec.status])
       
        table = Table(data=tableData)
        table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                   ('INNERGRID', (0, 0), (0, 1), 0.5, colors.black),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                   ('FONTSIZE', (0, 0), (-1, -1), 10),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        return table

    def applications_table(self, applications, language):
        if language == "es":
            tableData = [["VIAJE", "ESTADO"]]
            
        else:
            tableData = [["TRIP", "STATUS"]]

        for app in applications:
            tableData.append([app.trip.title, app.status])
       
        table = Table(data=tableData)
        table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                   ('INNERGRID', (0, 0), (0, 1), 0.5, colors.black),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                   ('FONTSIZE', (0, 0), (-1, -1), 10),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        return table

    def general_table(self, personal_table, created_trips_table, invitations_table, applications_table, language):
        sp = ParagraphStyle('parrafos',
                            alignment=TA_CENTER,
                            fontSize=12)
        story = []

        if language == "es":
            pa1 = Paragraph(u"Datos personales", sp)
            story.append(pa1)
            story.append(Spacer(0, 5))
            story.append(personal_table)
            story.append(Spacer(0, 20))

            if created_trips_table != "":
                pa2 = Paragraph(u"Datos de trips creados", sp)
                story.append(pa2)
                story.append(Spacer(0, 5))
                story.append(created_trips_table)
                story.append(Spacer(0, 20))

            if invitations_table != "":
                pa3 = Paragraph(u"Datos de peticiones", sp)
                story.append(pa3)
                story.append(Spacer(0, 5))
                story.append(invitations_table)
                story.append(Spacer(0, 20))

            if applications_table != "":
                pa4 = Paragraph(u"Datos de solicitudes", sp)
                story.append(pa4)
                story.append(Spacer(0, 5))
                story.append(applications_table)

        else:
            pa1 = Paragraph(u"Personal data", sp)
            story.append(pa1)
            story.append(Spacer(0, 5))
            story.append(personal_table)
            story.append(Spacer(0, 20))

            if created_trips_table != "":
                pa2 = Paragraph(u"Created trips data", sp)
                story.append(pa2)
                story.append(Spacer(0, 5))
                story.append(created_trips_table)
                story.append(Spacer(0, 20))

            if invitations_table != "":
                pa3 = Paragraph(u"Invitations data", sp)
                story.append(pa3)
                story.append(Spacer(0, 5))
                story.append(invitations_table)
                story.append(Spacer(0, 20))

            if applications_table != "":
                pa4 = Paragraph(u"Applications data", sp)
                story.append(pa4)
                story.append(Spacer(0, 5))
                story.append(applications_table)

        return story
        
    def post(self, request):
        user_id = request.data.get("user_id", "")
        language = request.data.get("language", "")

        user = User.objects.get(pk=user_id)
        userprofile = user.userprofile

        trips = Trip.objects.filter(user=userprofile)
        sended = Invitation.objects.filter(sender=userprofile)
        received = Invitation.objects.filter(receiver=userprofile)
        applications = Application.objects.filter(applicant=userprofile)
        
        name = os.path.join(settings.BASE_DIR, 'TravelMateServer') + '\static\exported_data_' + userprofile.get_full_name() + '.pdf'   
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']

        def header(canvas, doc):
            canvas.saveState()
            logo_img = 'https://s3.amazonaws.com/wayteam-static/static/img/logo.png'
            canvas.drawImage(logo_img, 40, 740, 120, 90, preserveAspectRatio=True)
            canvas.setFont("Helvetica", 16)
            canvas.drawString(230, 790, u"TRAVEL MATE")
            canvas.setFont("Helvetica", 14)
            
            if language == "es":
                canvas.drawString(218, 770, u"Sus datos exportados")
                date = str(time.strftime("%d/%m/%y %H:%M:%S"))
                canvas.setFont("Helvetica", 12)
                canvas.drawString(440, 780, date)

            else:
                canvas.drawString(227, 770, u"User data exported")
                date = str(time.strftime("%y-%m-%d %H:%M:%S"))
                canvas.setFont("Helvetica", 12)
                canvas.drawString(440, 780, date)
            canvas.restoreState()

        doc = BaseDocTemplate(name, pagesize=A4)
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height-1.5*cm, id='normal')
        template = PageTemplate(id='test', frames=frame, onPage=header)
        doc.addPageTemplates([template])

        personal_table = self.personal_table(user, userprofile, language)
        created_trips_table = ""
        invitations_table = ""
        applications_table = ""
        if trips:
            created_trips_table = self.created_trips_table(trips, language)
        if sended or received:
            invitations_table = self.invitations_table(sended, received, language)
        if applications:
            applications_table = self.applications_table(applications, language)

        story = self.general_table(personal_table, created_trips_table, invitations_table, applications_table, language)
        doc.build(story)

        if language == "es":  
            send_mail("Datos exportados", "Estos son los datos exportados de " + userprofile.get_full_name(), userprofile.email, name)
        else:  
            send_mail("Exported data", "This is the " + userprofile.get_full_name() + "'s exported data", userprofile.email, name)
        os.remove(name)
        return Response(status=200)


def backendWakeUp(request):
    return JsonResponse({'message':'Waking up backend'}, status=200)
