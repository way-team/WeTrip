from TravelMateServer.API.serializers import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, filters
from .models import UserProfile, Trip, Invitation, City, Rate, Application
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from datetime import datetime
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def get_user_by_token(request):
    key = request.data.get('token', '')
    tk = get_object_or_404(Token, key=key)
    user = tk.user
    user_profile = UserProfile.objects.get(user=user)

    return user_profile


class GetUserView(APIView):
    def post(self, request):
        userProfile = get_user_by_token(request)

        return Response(UserProfileSerializer(userProfile, many=False).data)


class RateUser(APIView):
    def post(self, request):

        # key = request.data.get('token', '')
        # tk = get_object_or_404(Token, key=key)
        # user = tk.user

        #username = request.user.username
        username = request.data.get('username', '')
        voter = User.objects.get(username="fran").userprofile

        votedUsername = request.data.get('voted', '')
        voted = User.objects.get(username=votedUsername).userprofile

        value = request.data.get('value', '')

        rate = Rate.objects.filter(voted=voted, voter=voter).first()
        if (rate == None):
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
            avgUserRating = sumRatings / userRatings.count()
            user.avarageRate = avgUserRating
            user.save()

        refreshUserAverageRating(voted)
        userProfile = UserProfile.objects.get(user=voted)

        return Response(UserProfileSerializer(voted, many=False).data)


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
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

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
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

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
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def post(self, request):
        """
        POST method
        """
        user = get_user_by_token(request)

        friends, pending = get_friends_or_pending(user)

        discover_people = []
        interests = user.interests.all()

        # First, we obtain the people with the same interests
        #for interest in interests:
        aux = UserProfile.objects.filter(interests__in=interests)
        for person in aux:
            if not person in discover_people:
                discover_people.append(person)

        # After, we obtain the people without the same interests
        # and append them at the end of the discover list
        all_users = list(UserProfile.objects.all())
        for person in discover_people:
            all_users.remove(person)
        for person in all_users:
            discover_people.append(person)

        # Finally, we remove from the discover list the people
        # who are our friends or pending friends
        for person in friends:
            discover_people.remove(person)
        for person in pending:
            discover_people.remove(person)
        discover_people.remove(user)

        return Response(UserProfileSerializer(discover_people, many=True).data)


class MyTripsList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = TripSerializer

    def get_queryset(self):
        return Trip.objects.filter(
            user__user=self.request.user).order_by('-startDate')


class AvailableTripsList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = TripSerializer

    def get_queryset(self):
        today = datetime.today()
        return Trip.objects.filter(
            Q(status=True) & Q(startDate__gte=today) & Q(
                tripType='PUBLIC')).exclude(
                    user__user=self.request.user).order_by('-startDate')


class AvailableTripsSearch(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    serializer_class = TripSerializer

    def get_queryset(self):
        today = datetime.today()
        return Trip.objects.filter(
            Q(status=True) & Q(startDate__gte=today) & Q(
                tripType='PUBLIC')).exclude(
                    user__user=self.request.user).order_by('-startDate')

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


class CreateTrip(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, SessionAuthentication)

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

        #GET CITY DATA
        cityId = request.data.get('city')

        #GET CITY
        city = City.objects.get(pk=cityId)
        image_name = city.country.name + '.jpg'

        try:
            userImage = request.data['file']
            trip = Trip(
                user=user,
                title=title,
                description=description,
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
                startDate=startDate,
                endDate=endDate,
                tripType=tripType,
                image=image_name)

            trip.save()
        finally:
            #GET CITY AND ADD TRIP
            city = City.objects.get(pk=cityId)
            city.trips.add(trip)

            return Response(TripSerializer(trip, many=False).data)


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
        trip = Trip.objects.get(pk=trip_id)

        return Response(TripSerializer(trip, many=False).data)


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
        user = get_user_by_token(request)

        trip_id = request.data.get("trip_id", "")
        title = request.data.get("title", "")
        description = request.data.get("description", "")
        start_date = request.data.get("start_date", "")
        end_date = request.data.get("end_date", "")
        trip_type = request.data.get("trip_type", "")

        city_id = request.data.get("city", "")

        city = City.objects.get(pk=city_id)
        image_name = city.country.name + '.jpg'

        stored_trip = Trip.objects.get(pk=trip_id)
        stored_creator = stored_trip.user
        if stored_creator != user:
            raise ValueError("You are not the creator of this trip")

        stored_cities = stored_trip.cities.all()

        try:
            user_image = request.data['file']
            trip = Trip(
                id=trip_id,
                user=user,
                title=title,
                description=description,
                startDate=start_date,
                endDate=end_date,
                tripType=trip_type,
                image=image_name,
                userImage=user_image)
            trip.save()

        except MultiValueDictKeyError:
            trip = Trip(
                id=trip_id,
                user=user,
                title=title,
                description=description,
                startDate=start_date,
                endDate=end_date,
                tripType=trip_type,
                image=image_name)
            trip.save()

        finally:
            if not city in stored_cities:
                city.trips.add(stored_trip)

        return Response(TripSerializer(stored_trip, many=False).data)


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

        trip_id = request.data.get("trip_id", "")
        trip = Trip.objects.get(pk=trip_id)

        try:
            query = Application.objects.filter(trip=trip).get(applicant=user)
        except Application.DoesNotExist:
            query = None

        if query is None:
            application = Application(applicant=user, trip=trip, status="P")
            application.save()
        else:
            raise ValueError("You have already applied to this trip")

        return Response(TripSerializer(trip, many=False).data)


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
