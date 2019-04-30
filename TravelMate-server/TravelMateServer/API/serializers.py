from .models import UserProfile, Language, Trip, Application, City, Country, Interest, Message, Invitation
from rest_framework import serializers
from django.contrib.auth.models import User
import datetime


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_staff']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name']


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['applicant', 'status', 'id']


class TripSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    userImage = serializers.SerializerMethodField()
    applications_count = serializers.SerializerMethodField()
    cities_count = serializers.SerializerMethodField()
    cities = serializers.SlugRelatedField(
        many=True, queryset=City.objects.all(), slug_field='name')

    class Meta:
        model = Trip
        fields = [
            'id', 'creator', 'title', 'description','price', 'startDate', 'endDate',
            'tripType', 'image', 'userImage', 'status', 'applications_count',
            'cities_count', 'cities'
        ]

    def get_creator(self, obj):
        user_queryset = obj.user.user.username
        return user_queryset

    def get_userImage(self, obj):
        userImage_queryset = obj.userImage.name
        return userImage_queryset

    def get_applications_count(self, obj):
        return obj.applications.count()

    def get_cities_count(self, obj):
        return obj.cities.count()


class FullTripSerializer(serializers.Serializer):
    trip = TripSerializer(many=False)
    applicationsList = ApplicationSerializer(many=True)
    pendingsList = ApplicationSerializer(many=True)
    rejectedList = ApplicationSerializer(many=True)


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    trips = TripSerializer(many=True)

    class Meta:
        model = City
        fields = ['country', 'trips', 'name', 'id']


class CityReducedSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    trips_count = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['country', 'trips_count', 'name', 'id']

    def get_trips_count(self, obj):
        return obj.trips.count()


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    languages = serializers.SlugRelatedField(
        many=True, queryset=Language.objects.all(), slug_field='name')
    interests = serializers.SlugRelatedField(
        many=True, queryset=Interest.objects.all(), slug_field='name')

    created_trips = serializers.SerializerMethodField()

    past_joined_trips = serializers.SerializerMethodField()

    future_joined_trips = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'user', 'email', 'first_name', 'last_name', 'description',
            'birthdate', 'city', 'nationality', 'photo', 'discoverPhoto',
            'avarageRate', 'numRate', 'isPremium', 'status','profesion','civilStatus', 'gender',
            'languages', 'interests', 'created_trips', 'past_joined_trips',
            'future_joined_trips', 
        ]

    def get_created_trips(self, obj):
        trip_queryset = obj.trip_set.all()
        return TripSerializer(trip_queryset, many=True).data


    def get_past_joined_trips(self, obj):
        today = datetime.datetime.now().date()

        applicant = obj
        myApplications = Application.objects.filter(applicant = applicant, status = 'A')
        myTrips = []
        for app in myApplications:
            if app.trip.startDate < today and app.trip.status == True and app.trip.tripType == "PUBLIC":
                myTrips.append(app.trip)

        createdTrips = Trip.objects.filter(user=applicant, startDate__lt = today, status = True, tripType = 'PUBLIC')

        for trip in createdTrips:
            myTrips.append(trip)

        myTrips.sort(key=lambda x: x.startDate, reverse=True)

        return TripSerializer(myTrips, many=True).data


    def get_future_joined_trips(self, obj):
        today = datetime.datetime.now().date()

        applicant = obj
        myApplications = Application.objects.filter(applicant = applicant, status = 'A')
        myTrips = []
        for app in myApplications:
            if app.trip.startDate > today and app.trip.status == True and app.trip.tripType == "PUBLIC":
                myTrips.append(app.trip)

        createdTrips = Trip.objects.filter(user=applicant, startDate__gte = today, status = True, tripType = 'PUBLIC')

        for trip in createdTrips:
            myTrips.append(trip)

        myTrips.sort(key=lambda x: x.startDate, reverse=True)

        return TripSerializer(myTrips, many=True).data
   



class FullUserProfileSerializer(serializers.Serializer):
    user = UserProfileSerializer(many = False)
    pastTrips = TripSerializer(many = True)
    futureTrips = TripSerializer(many = True)


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(
        many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']


class InterestSerializer(serializers.ModelSerializer):
    users = UserProfileSerializer(many=True)

    class Meta:
        model = Interest
        fields = ['name', 'users']


class InterestNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['name']


class InterestReducedSerializer(serializers.ModelSerializer):
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = Interest
        fields = ['name', 'users_count']

    def get_users_count(self, obj):
        return obj.users.count()


class InvitationSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(many=False)
    receiver = UserProfileSerializer(many=False)

    class Meta:
        model = Invitation
        fields = ['sender', 'receiver', 'status']
