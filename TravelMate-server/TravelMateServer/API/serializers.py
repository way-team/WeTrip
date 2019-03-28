from .models import UserProfile, Language, Trip, Application, City, Country
from rest_framework import serializers
from django.contrib.auth.models import User


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

    class Meta:
        model = Trip
        fields = [
            'creator', 'title', 'description', 'startDate', 'endDate',
            'tripType', 'image', 'status'
        ]

    def get_creator(self, obj):
        user_queryset = obj.user.user.username
        return user_queryset


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
    interest_set = serializers.SlugRelatedField(
        many=True, queryset=Language.objects.all(), slug_field='name')

    created_trips = serializers.SerializerMethodField()

    joined_trips = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'user', 'email', 'first_name', 'last_name', 'description',
            'birthdate', 'city', 'nationality', 'photo', 'discoverPhoto',
            'avarageRate', 'numRate', 'isPremium', 'status', 'gender',
            'languages', 'interest_set', 'created_trips', 'joined_trips'
        ]

    def get_created_trips(self, obj):
        trip_queryset = obj.trip_set.all()
        return TripSerializer(trip_queryset, many=True).data

    def get_joined_trips(self, obj):
        trip_queryset = Trip.objects.filter(
            applications__applicant=obj, applications__status="A")

        return TripSerializer(trip_queryset, many=True).data
