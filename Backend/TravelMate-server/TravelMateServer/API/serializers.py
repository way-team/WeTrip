from .models import UserProfile, Language
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    languages = serializers.SlugRelatedField(
        many=True, queryset=Language.objects.all(), slug_field='name')

    class Meta:
        model = UserProfile
        fields = [
            'user', 'email', 'first_name', 'last_name', 'description',
            'birthdate', 'city', 'nationality', 'photo', 'discoverPhoto',
            'avarageRate', 'numRate', 'isPremium', 'status', 'gender',
            'languages'
        ]
