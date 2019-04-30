import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .models import Trip, UserProfile, Language, City, Country, Interest, Application
from .serializers import TripSerializer



class TravelMateTests(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.lang1 = Language.objects.create(name='english')
        cls.lang2 = Language.objects.create(name='spanish')
        cls.lang3 = Language.objects.create(name='bulgarian')
        cls.lang4 = Language.objects.create(name='chinese')
        cls.lang5 = Language.objects.create(name='french')

        cls.user1 = User.objects.create_user(username='user1', password='user1', email=None)
        cls.user2 = User.objects.create_user(username='user2', password='user2', email=None)
        cls.user3 = User.objects.create_user(username='user3', password='user3', email=None)
        cls.user4 = User.objects.create_user(username='user4', password='user4', email=None)
        cls.user5 = User.objects.create_user(username='user5', password='user5', email=None)
        cls.user6 = User.objects.create_user(username='user6', password='user6', email=None)

        cls.userprofile1 = UserProfile.objects.create(user=cls.user1, email='user1@gmail.com', first_name='user1', last_name='user1', birthdate='1991-03-30', nationality='spanish', avarageRate=4, numRate=2, isPremium=False, gender='M', status='A')
        cls.userprofile2 = UserProfile.objects.create(user=cls.user2, email='user2@gmail.com', first_name='user2', last_name='user2', birthdate='1983-06-11', nationality='spanish', avarageRate=3, numRate=1, isPremium=False, gender='W', status='A')
        cls.userprofile3 = UserProfile.objects.create(user=cls.user3, email='user3@gmail.com', first_name='user3', last_name='user3', birthdate='1979-05-15', nationality='english', avarageRate=3, numRate=1, isPremium=False, gender='W', status='A')
        cls.userprofile4 = UserProfile.objects.create(user=cls.user4, email='user4@gmail.com', first_name='user4', last_name='user4', birthdate='1978-11-04', nationality='spanish', avarageRate=2, numRate=1, isPremium=False, gender='M', status='A')
        cls.userprofile5 = UserProfile.objects.create(user=cls.user5, email='user5@gmail.com', first_name='user5', last_name='user5', birthdate='1993-12-04', nationality='french', avarageRate=2, numRate=1, isPremium=True, gender='M', status='A')
        cls.userprofile6 = UserProfile.objects.create(user=cls.user6, email='user6@gmail.com', first_name='user6', last_name='user6', birthdate='1990-08-23', nationality='chinese', avarageRate=5, numRate=1, isPremium=True, gender='W', status='D')
        
        cls.userprofile1.languages.add(cls.lang1, cls.lang2)
        cls.userprofile2.languages.add(cls.lang2)
        cls.userprofile3.languages.add(cls.lang1, cls.lang5)
        cls.userprofile4.languages.add(cls.lang2, cls.lang3)
        cls.userprofile5.languages.add(cls.lang5)
        cls.userprofile6.languages.add(cls.lang1, cls.lang3, cls.lang4)

        
        cls.trip1 = Trip.objects.create(user=cls.userprofile1, title='trip1', startDate='2019-09-21', endDate='2019-10-02', tripType='PUBLIC')
        cls.trip2 = Trip.objects.create(user=cls.userprofile1, title='trip2', startDate='2019-02-03', endDate='2019-02-06', tripType='PUBLIC')
        cls.trip3 = Trip.objects.create(user=cls.userprofile2, title='trip3', startDate='2019-09-20', endDate='2019-09-30', tripType='PUBLIC')
        cls.trip4 = Trip.objects.create(user=cls.userprofile2, title='trip4', startDate='2019-12-20', endDate='2019-12-31', tripType='PRIVATE')
        cls.trip5 = Trip.objects.create(user=cls.userprofile2, title='trip5', startDate='2018-07-18', endDate='2018-07-24', tripType='PUBLIC')
        cls.trip6 = Trip.objects.create(user=cls.userprofile3, title='trip6', startDate='2020-04-05', endDate='2020-04-06', tripType='PUBLIC')
        cls.trip7 = Trip.objects.create(user=cls.userprofile3, title='trip7', startDate='2019-01-20', endDate='2019-01-25', tripType='PUBLIC')
        cls.trip8 = Trip.objects.create(user=cls.userprofile3, title='trip8', startDate='2019-06-03', endDate='2019-06-12', tripType='PUBLIC')
        cls.trip9 = Trip.objects.create(user=cls.userprofile4, title='trip9', startDate='2019-07-03', endDate='2019-07-19', tripType='PUBLIC')
        cls.trip10 = Trip.objects.create(user=cls.userprofile4, title='trip10', startDate='2019-08-15', endDate='2019-08-18', tripType='PUBLIC')
        cls.trip11 = Trip.objects.create(user=cls.userprofile5, title='trip11', startDate='2020-01-03', endDate='2020-01-13', tripType='PUBLIC')
        cls.trip12 = Trip.objects.create(user=cls.userprofile5, title='trip12', startDate='2019-09-17', endDate='2019-09-24', tripType='PRIVATE')

        cls.country1 = Country.objects.create(name='Spain')
        cls.country2 = Country.objects.create(name='England')
        cls.country3 = Country.objects.create(name='Bulgaria')
        cls.country4 = Country.objects.create(name='France')

        cls.city1 = City.objects.create(name='Madrid', country=cls.country1)
        cls.city2 = City.objects.create(name='Barcelona', country=cls.country1)
        cls.city3 = City.objects.create(name='Sevilla', country=cls.country1)
        cls.city4 = City.objects.create(name='London', country=cls.country2)
        cls.city5 = City.objects.create(name='Sofia', country=cls.country3)
        cls.city6 = City.objects.create(name='Paris', country=cls.country4)

        cls.city1.trips.add(cls.trip1, cls.trip7)
        cls.city2.trips.add(cls.trip2, cls.trip8)
        cls.city3.trips.add(cls.trip3, cls.trip9)
        cls.city4.trips.add(cls.trip4, cls.trip10)
        cls.city5.trips.add(cls.trip5, cls.trip11)
        cls.city6.trips.add(cls.trip6, cls.trip12)

        cls.interest1 = Interest.objects.create(name='football')
        cls.interest2 = Interest.objects.create(name='cooking')
        cls.interest3 = Interest.objects.create(name='skydiving')
        cls.interest4 = Interest.objects.create(name='running')
        cls.interest5 = Interest.objects.create(name='museums')
        cls.interest6 = Interest.objects.create(name='shopping')
        cls.interest7 = Interest.objects.create(name='swimming')
        cls.interest8 = Interest.objects.create(name='tennis')

        cls.interest1.users.add(cls.userprofile1)
        cls.interest2.users.add(cls.userprofile2)
        cls.interest3.users.add(cls.userprofile4)
        cls.interest4.users.add(cls.userprofile2)
        cls.interest5.users.add(cls.userprofile2)
        cls.interest6.users.add(cls.userprofile5)
        cls.interest7.users.add(cls.userprofile3, cls.userprofile4, cls.userprofile5)
        cls.interest8.users.add(cls.userprofile1, cls.userprofile2)

        cls.application1 = Application.objects.create(applicant=cls.userprofile1, trip=cls.trip9, status='A')
        cls.application2 = Application.objects.create(applicant=cls.userprofile2, trip=cls.trip11, status='P')
        cls.application3 = Application.objects.create(applicant=cls.userprofile3, trip=cls.trip8, status='R')
        cls.application4 = Application.objects.create(applicant=cls.userprofile3, trip=cls.trip9, status='A')

        
        

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    def test_my_trips_list(self):
        
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        response = self.client.get(reverse('my_trips_list'))
        self.assertEqual(200, response.status_code)
        jsonResponse = response.json()
        self.assertTrue(jsonResponse['count'] == 2)
        myTrips = []
        myTrips.append(self.trip1)
        myTrips.append(self.trip2)
        serializer = TripSerializer(myTrips, many=True)
        self.assertEqual(jsonResponse['results'], serializer.data)
    
        self.user = self.user3
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        response = self.client.get(reverse('my_trips_list'))
        self.assertEqual(200, response.status_code)
        jsonResponse = response.json()
        self.assertTrue(jsonResponse['count'] == 3)
        myTrips = []
        myTrips.append(self.trip6)
        myTrips.append(self.trip8)
        myTrips.append(self.trip7)
        serializer = TripSerializer(myTrips, many=True)
        self.assertEqual(jsonResponse['results'], serializer.data)

    def test_available_trips_list(self):
        
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        response = self.client.get(reverse('available_trips_list'))
        self.assertEqual(200, response.status_code)
        jsonResponse = response.json()
        self.assertTrue(jsonResponse['count'] == 5)
        myTrips = []
        myTrips.append(self.trip11)
        myTrips.append(self.trip3)
        myTrips.append(self.trip6)
        myTrips.append(self.trip8)
        myTrips.append(self.trip10)
        serializer = TripSerializer(myTrips, many=True)
        self.assertEqual(jsonResponse['results'], serializer.data)
    
        

       
    

        
     
