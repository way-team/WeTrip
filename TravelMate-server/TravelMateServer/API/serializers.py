from .models import UserProfile, Language, Trip, Application, City, Country, Interest, Message
from rest_framework import serializers
from django.contrib.auth.models import User
import datetime


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name']


class TripSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    userImage = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = [
            'id', 'creator', 'title', 'description', 'startDate', 'endDate',
            'tripType', 'image', 'userImage', 'status'
        ]

    def get_creator(self, obj):
        user_queryset = obj.user.user.username
        return user_queryset

    def get_userImage(self, obj):
        userImage_queryset = obj.userImage.name
        return userImage_queryset


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    trips = TripSerializer(many=True)

    class Meta:
        model = City
        fields = ['country', 'trips', 'name', 'id']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    languages = serializers.SlugRelatedField(
        many=True, queryset=Language.objects.all(), slug_field='name')
    interests = serializers.SlugRelatedField(
        many=True, queryset=Interest.objects.all(), slug_field='name')

    created_trips = serializers.SerializerMethodField()

    past_joined_trips = serializers.SerializerMethodField()

    future_joined_trips = serializers.SerializerMethodField()

    active_joined_trips = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'user', 'email', 'first_name', 'last_name', 'description',
            'birthdate', 'city', 'nationality', 'photo', 'discoverPhoto',
            'avarageRate', 'numRate', 'isPremium', 'status', 'gender',
            'languages', 'interests', 'created_trips', 'past_joined_trips',
            'future_joined_trips', 'active_joined_trips'
        ]

    def get_created_trips(self, obj):
        trip_queryset = obj.trip_set.all()
        return TripSerializer(trip_queryset, many=True).data

    def get_past_joined_trips(self, obj):
        now = datetime.datetime.now()

        trip_queryset = Trip.objects.filter(
            applications__applicant=obj,
            applications__status="A",
            endDate__lte=now,
            startDate__lte=now)

        return TripSerializer(trip_queryset, many=True).data

    def get_future_joined_trips(self, obj):
        now = datetime.datetime.now()

        trip_queryset = Trip.objects.filter(
            applications__applicant=obj,
            applications__status="A",
            endDate__gte=now,
            startDate__gte=now)

        return TripSerializer(trip_queryset, many=True).data

    def get_active_joined_trips(self, obj):
        now = datetime.datetime.now()

        trip_queryset = Trip.objects.filter(
            applications__applicant=obj,
            applications__status="A",
            endDate__lte=now,
            startDate__gte=now)

        return TripSerializer(trip_queryset, many=True).data


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(
        many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']
