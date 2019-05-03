import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .models import Trip, UserProfile, Language, City, Country, Interest, Application, Invitation, Rate
from .serializers import TripSerializer
from .serializers import LanguageSerializer
from .serializers import *





class TravelMateTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Creating a Test Scenario"""

        # In this method we will create all objects that we will be using to perform the functional tests

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

        cls.userprofile1 = UserProfile.objects.create(user=cls.user1, email='user1@gmail.com', first_name='user1', last_name='user1', birthdate='1991-03-30', nationality='spanish', avarageRate=4, numRate=2, isPremium=False , gender='M', status='A', civilStatus='S')
        cls.userprofile2 = UserProfile.objects.create(user=cls.user2, email='user2@gmail.com', first_name='user2', last_name='user2', birthdate='1983-06-11', nationality='spanish', avarageRate=3, numRate=1, isPremium=False, gender='W', status='A', civilStatus='D')
        cls.userprofile3 = UserProfile.objects.create(user=cls.user3, email='user3@gmail.com', first_name='user3', last_name='user3', birthdate='1979-05-15', nationality='english', avarageRate=3, numRate=1, isPremium=False, gender='W', status='A', civilStatus='W')
        cls.userprofile4 = UserProfile.objects.create(user=cls.user4, email='user4@gmail.com', first_name='user4', last_name='user4', birthdate='1978-11-04', nationality='spanish', avarageRate=2, numRate=1, isPremium=False, gender='M', status='A', civilStatus='M')
        cls.userprofile5 = UserProfile.objects.create(user=cls.user5, email='user5@gmail.com', first_name='user5', last_name='user5', birthdate='1993-12-04', nationality='french', avarageRate=2, numRate=1, isPremium=True, gender='M', status='A', civilStatus='R')
        cls.userprofile6 = UserProfile.objects.create(user=cls.user6, email='user6@gmail.com', first_name='user6', last_name='user6', birthdate='1990-08-23', nationality='chinese', avarageRate=0, numRate=0, isPremium=True, gender='W', status='D', civilStatus='S')
        
        cls.userprofile1.languages.add(cls.lang1, cls.lang2)
        cls.userprofile2.languages.add(cls.lang2)
        cls.userprofile3.languages.add(cls.lang1, cls.lang5)
        cls.userprofile4.languages.add(cls.lang2, cls.lang3)
        cls.userprofile5.languages.add(cls.lang5)
        cls.userprofile6.languages.add(cls.lang1, cls.lang3, cls.lang4)

        
        cls.trip1 = Trip.objects.create(user=cls.userprofile1, title='trip1', description='mountains', startDate='2019-09-21', endDate='2019-10-02', tripType='PUBLIC')
        cls.trip2 = Trip.objects.create(user=cls.userprofile1, title='trip2', description='cruise', startDate='2019-02-03', endDate='2019-02-06', tripType='PUBLIC')
        cls.trip3 = Trip.objects.create(user=cls.userprofile2, title='trip3', description='mountain', startDate='2019-09-20', endDate='2019-09-30', tripType='PUBLIC')
        cls.trip4 = Trip.objects.create(user=cls.userprofile2, title='trip4', description='beach', startDate='2019-12-20', endDate='2019-12-31', tripType='PRIVATE')
        cls.trip5 = Trip.objects.create(user=cls.userprofile2, title='trip5', description='mountains', startDate='2018-07-18', endDate='2018-07-24', tripType='PUBLIC')
        cls.trip6 = Trip.objects.create(user=cls.userprofile3, title='trip6', description='wonderful experience', startDate='2020-04-05', endDate='2020-04-06', tripType='PUBLIC')
        cls.trip7 = Trip.objects.create(user=cls.userprofile3, title='trip7', description='journey', startDate='2019-01-20', endDate='2019-01-25', tripType='PUBLIC')
        cls.trip8 = Trip.objects.create(user=cls.userprofile3, title='trip8', description='mountain', startDate='2019-06-03', endDate='2019-06-12', tripType='PUBLIC')
        cls.trip9 = Trip.objects.create(user=cls.userprofile4, title='trip9', startDate='2019-07-03', endDate='2019-07-19', tripType='PUBLIC')
        cls.trip10 = Trip.objects.create(user=cls.userprofile4, title='trip10', description='snow, skiing, mountains', startDate='2019-08-15', endDate='2019-08-18', tripType='PUBLIC')
        cls.trip11 = Trip.objects.create(user=cls.userprofile5, title='trip11', description='beach, sun, sea', startDate='2020-01-03', endDate='2020-01-13', tripType='PUBLIC')
        cls.trip12 = Trip.objects.create(user=cls.userprofile5, title='trip12', description='low-cost', startDate='2019-09-17', endDate='2019-09-24', tripType='PRIVATE')

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
        cls.interest6.users.add(cls.userprofile5,cls.userprofile2, cls.userprofile4,cls.userprofile1)
        cls.interest7.users.add(cls.userprofile3, cls.userprofile4, cls.userprofile5)
        cls.interest8.users.add(cls.userprofile1, cls.userprofile2)

        cls.application1 = Application.objects.create(applicant=cls.userprofile1, trip=cls.trip9, status='A')
        cls.application2 = Application.objects.create(applicant=cls.userprofile2, trip=cls.trip11, status='P')
        cls.application3 = Application.objects.create(applicant=cls.userprofile5, trip=cls.trip8, status='R')
        cls.application4 = Application.objects.create(applicant=cls.userprofile5, trip=cls.trip9, status='A')

        cls.invitation1 = Invitation.objects.create(sender=cls.userprofile1, receiver=cls.userprofile2, status='A')
        cls.invitation2 = Invitation.objects.create(sender=cls.userprofile2, receiver=cls.userprofile4, status='P')
        cls.invitation3 = Invitation.objects.create(sender=cls.userprofile3, receiver=cls.userprofile4, status='R')
        cls.invitation4 = Invitation.objects.create(sender=cls.userprofile5, receiver=cls.userprofile1, status='P')
        cls.invitation5 = Invitation.objects.create(sender=cls.userprofile5, receiver=cls.userprofile2, status='A')
        cls.invitation6 = Invitation.objects.create(sender=cls.userprofile2, receiver=cls.userprofile3, status='A')
        cls.invitation7 = Invitation.objects.create(sender=cls.userprofile4, receiver=cls.userprofile1, status='A')

        cls.rate1 = Rate.objects.create(voter=cls.userprofile1, voted=cls.userprofile2, value=3)
        cls.rate2 = Rate.objects.create(voter=cls.userprofile2, voted=cls.userprofile1, value=4)
        cls.rate3 = Rate.objects.create(voter=cls.userprofile2, voted=cls.userprofile3, value=3)
        cls.rate4 = Rate.objects.create(voter=cls.userprofile1, voted=cls.userprofile4, value=2)
        cls.rate5 = Rate.objects.create(voter=cls.userprofile4, voted=cls.userprofile1, value=4)
        cls.rate6 = Rate.objects.create(voter=cls.userprofile2, voted=cls.userprofile5, value=2)
  
        

    def api_authentication(self):
        """This is the authentication method"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    def test_my_trips_list(self):
        """The method 'my_trips_list' has to return a list with all the trips created by the current user ordered by their start date."""

        # We log in as 'user1'
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        response = self.client.get(reverse('my_trips_list'))

        # We check the status code of the request
        self.assertEqual(200, response.status_code)

        # user1 has created 2 trips. Let's check this:
        jsonResponse = response.json()
        self.assertTrue(jsonResponse['count'] == 2)

        # The 2 trips that user1 has created are 'trip1' and 'trip2'. 'trip1' should appear first. Let's check this: 
        myTrips = []
        myTrips.append(self.trip1)
        myTrips.append(self.trip2)
        serializer = TripSerializer(myTrips, many=True)
        self.assertEqual(jsonResponse['results'], serializer.data)
    
        #------------------------------------------------------------------------------------------

        # We log in as 'user3'
        self.user = self.user3
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        response = self.client.get(reverse('my_trips_list'))

        # We check the status code of the request
        self.assertEqual(200, response.status_code)

        # user3 has created 3 trips. Let's check this:
        jsonResponse = response.json()
        self.assertTrue(jsonResponse['count'] == 3)

        # The 3 trips that user3 has created are 'trip6', 'trip7' and 'trip8'. They should be ordered correctly. Let's check this:
        myTrips = []
        myTrips.append(self.trip6)
        myTrips.append(self.trip8)
        myTrips.append(self.trip7)
        serializer = TripSerializer(myTrips, many=True)
        self.assertEqual(jsonResponse['results'], serializer.data)


    def test_available_trips_list(self):
        """The method 'available_trips_list' return all available trips to the current user. A trip is considered 'avaiable' if:
          1) It has not been marked as 'deleted' (status = True)
          2) Its start date is in the future
          3) It is public
          4) Its creator is not the current user, but another user
          5) There is no application with 'Rejected' status that refers the current user to the trip.
        """

        # We log in as user1
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        response = self.client.get(reverse('available_trips_list'))

        #Let's check the status code of the request
        self.assertEqual(200, response.status_code)

        #There must be 6 available trips. 
        jsonResponse = response.json()
        self.assertTrue(jsonResponse['count'] == 6)

        #'trip11' should appear first in the list, because it has been created by a premium user. The rest of the available trips are: 'trip3', 'trip6', 'trip8', 'trip9' and 'trip10'
        myTrips = []
        myTrips.append(self.trip11)
        myTrips.append(self.trip3)
        myTrips.append(self.trip6)
        myTrips.append(self.trip8)
        myTrips.append(self.trip9)
        myTrips.append(self.trip10)
        serializer = TripSerializer(myTrips, many=True)
        self.assertEqual(jsonResponse['results'], serializer.data)



    def test_available_trips_search(self):
        """The method 'available_trips_search' returns all available trips to the current user that contain the chosen key word in their title or description. A trip is considered 'avaiable' if:
          1) It has not been marked as 'deleted' (status = True)
          2) Its start date is in the future
          3) It is public
          4) Its creator is not the current user, but another user
          5) There is no application with 'Rejected' status that refers the current user to the trip.
        """

        # We log in as user5
        self.user = self.user5
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        # user5 wants to see all available trips that contain the word 'mountain'
        response = self.client.get('/trips/search/?search=mountain')

        #Let's check the status code of the request
        self.assertEqual(200, response.status_code)

        #There must be only 3 results. There are 5 available trips for user5, but only trip1, trip3 and trip10 match the search criteria. 
        #There are other trips that contain the key word 'mountain' in their description (like trip5 and trip8), but they are not 'available'.
        jsonResponse = response.json()
        self.assertTrue(jsonResponse['count'] == 3)

        myTrips = []
        myTrips.append(self.trip1)
        myTrips.append(self.trip3)
        myTrips.append(self.trip10)
        serializer = TripSerializer(myTrips, many=True)
        self.assertEqual(jsonResponse['results'], serializer.data)
        

    def test_apply_trip(self):
        """ The method 'apply_trip' allows user to apply for available trips."""
        
        #We log in as user2
        self.user = self.user2
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        #Let's see the current number of applications
        numApplicationsBefore = Application.objects.count()

        data = {"token":self.token.key, "trip_id": "11"}
        #user2 has already applied for trip11.
        
        with self.assertRaisesMessage(ValueError, "You can't apply for this trip."):
            response = self.client.post(reverse('apply_trip'), data=json.dumps(data), content_type='application/json')
        
        # We see that nothing has changed
        numApplicationsAfter = Application.objects.count()
        self.assertEqual(numApplicationsBefore, numApplicationsAfter)
        
        #------------------------------------------------------------------------------------------


        # We are still logged as user2
     
        #Let's see the current number of applications
        numApplicationsBefore = Application.objects.count()

        data = {"token":self.token.key, "trip_id": "5"}
        #user2 can't apply for trip5 because trip5 has already finished
        
        with self.assertRaisesMessage(ValueError, "You can't apply for this trip."):
            response = self.client.post(reverse('apply_trip'), data=json.dumps(data), content_type='application/json')
        
        # We see that nothing has changed
        numApplicationsAfter = Application.objects.count()
        self.assertEqual(numApplicationsBefore, numApplicationsAfter)
        
        #------------------------------------------------------------------------------------------

        # We are still logged as user2
      
        #Let's see the current number of applications
        numApplicationsBefore = Application.objects.count()

        data = {"token":self.token.key, "trip_id": "12"}
        #user2 can't apply for trip12 because trip12 is private.
        
        with self.assertRaisesMessage(ValueError, "You can't apply for this trip."):
            response = self.client.post(reverse('apply_trip'), data=json.dumps(data), content_type='application/json')
        
        # We see that nothing has changed
        numApplicationsAfter = Application.objects.count()
        self.assertEqual(numApplicationsBefore, numApplicationsAfter)
        
        #------------------------------------------------------------------------------------------

        # We are still logged as user2
        data = {"token":self.token.key, "trip_id": "6"}

        #user2 can apply for trip6
        response = self.client.post(reverse('apply_trip'), data=json.dumps(data), content_type='application/json')
       
        self.assertEqual(200, response.status_code)

        #We see that now there is a new application in the system.
        numApplicationsAfter = Application.objects.count()
        self.assertEqual(numApplicationsBefore+1, numApplicationsAfter)

    def test_accept_application(self):
        """ The method 'accept_application' is used to accept an application sent from another user for a trip."""
        
        #We log in as user2
        self.user = self.user2
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        data = {"token":self.token.key, "application_id": "2"}
        # application2 is an application for trip11. user2 is not the creator of this trip.

        # Let's check the current status of the application
        statusBefore = Application.objects.get(pk=2).status
        self.assertEqual(statusBefore, 'P')

        with self.assertRaisesMessage(ValueError, "You are not the creator of the application's trip"):
            response = self.client.post(reverse('accept_application'), data=json.dumps(data), content_type='application/json')

        # We see that the status hasn't changed.
        statusAfter = Application.objects.get(pk=2).status
        self.assertEqual(statusAfter, 'P')

        #------------------------------------------------------------------------------------------

        # We log in as user3
        self.user = self.user3
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        data = {"token":self.token.key, "application_id": "3"}
        # application3 has already been rejected. It cannot be accepted anymore.

        # Let's check the current status of the application
        statusBefore = Application.objects.get(pk=3).status
        self.assertEqual(statusBefore, 'R')

        with self.assertRaisesMessage(ValueError, "The application has just accepted or rejected"):
            response = self.client.post(reverse('accept_application'), data=json.dumps(data), content_type='application/json')

        # We see that the status hasn't changed.
        statusAfter = Application.objects.get(pk=3).status
        self.assertEqual(statusAfter, 'R')

        #------------------------------------------------------------------------------------------

        # We log in as user5
        self.user = self.user5
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        data = {"token":self.token.key, "application_id": "2"}
        #application2 is an application for trip11. user5 is the creator of this trip. He/she should be able to accept the application

        # Let's check the current status of the application
        statusBefore = Application.objects.get(pk=2).status
        self.assertEqual(statusBefore, 'P')

        response = self.client.post(reverse('accept_application'), data=json.dumps(data), content_type='application/json')
       
        self.assertEqual(200, response.status_code)

        #The application has been accepted.
        statusAfter = Application.objects.get(pk=2).status
        self.assertEqual(statusAfter, 'A')


    def test_reject_application(self):
        """ The method 'reject_application' is used to reject a application sent from another user for a trip."""
        
        # We log in as user2
        self.user = self.user2
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        data = {"token":self.token.key, "application_id": "2"}
        # application2 is an application for trip11. user2 is not the creator of this trip.

        # Let's check the current status of the application
        statusBefore = Application.objects.get(pk=2).status
        self.assertEqual(statusBefore, 'P')

        with self.assertRaisesMessage(ValueError, "You are not the creator of the application's trip"):
            response = self.client.post(reverse('reject_application'), data=json.dumps(data), content_type='application/json')

        # We see that the status hasn't changed.
        statusAfter = Application.objects.get(pk=2).status
        self.assertEqual(statusAfter, 'P')

        #------------------------------------------------------------------------------------------

        #We log in as user4
        self.user = self.user4
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        data = {"token":self.token.key, "application_id": "1"}
        #application1 has already been accepted

        # Let's check the current status of the application
        statusBefore = Application.objects.get(pk=1).status
        self.assertEqual(statusBefore, 'A')

        with self.assertRaisesMessage(ValueError, "The application has just accepted or rejected"):
            response = self.client.post(reverse('reject_application'), data=json.dumps(data), content_type='application/json')

         # We see that the status hasn't changed.
        statusAfter = Application.objects.get(pk=1).status
        self.assertEqual(statusAfter, 'A')

        #------------------------------------------------------------------------------------------

        # We log in as user5
        self.user = self.user5
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        data = {"token":self.token.key, "application_id": "2"}
        #application2 is an application for trip11. user5 is the creator of this trip. He/she should be able to reject the application

        # Let's check the current status of the application
        statusBefore = Application.objects.get(pk=2).status
        self.assertEqual(statusBefore, 'P')

        response = self.client.post(reverse('reject_application'), data=json.dumps(data), content_type='application/json')
       
        self.assertEqual(200, response.status_code)

        # We see that the application has been rejected successfully.
        statusAfter = Application.objects.get(pk=2).status
        self.assertEqual(statusAfter, 'R')



    def test_send_invitation(self):
        """The method 'send_invitation' allows users to send a friend request to another user"""
       
        # We log in as user1
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        # Let's check the current number of friend requests
        numInvitationsBefore = Invitation.objects.count()
        
        # user1 wants to send a friend request to user5. However, user5 has already sent a friend request to user1 (with PENDING status)
        data = {"token":self.token.key, "username": "user5"}
        
        with self.assertRaisesMessage(ValueError, 'This person has sent you a friend request before'):
            response = self.client.post(reverse('send_invitation'), data=json.dumps(data), content_type='application/json')
        
        # We see that nothing has changed
        numInvitationsAfter = Invitation.objects.count()
        self.assertEqual(numInvitationsBefore, numInvitationsAfter)

        #------------------------------------------------------------------------------------------

        # We log in as us user3
        self.user = self.user3
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        # Let's check the current number of friend requests
        numInvitationsBefore = Invitation.objects.count()

        #User3 wants to send a friend request to user4. But user4 has already rejected a friend request from user3.
        data = {"token":self.token.key, "username": "user4"}
        
        with self.assertRaisesMessage(ValueError, 'This person has rejected you'):
            response = self.client.post(reverse('send_invitation'), data=json.dumps(data), content_type='application/json')
             
        # We see that nothing has changed 
        numInvitationsAfter = Invitation.objects.count()
        self.assertEqual(numInvitationsBefore, numInvitationsAfter)

        #------------------------------------------------------------------------------------------

        #We log in as user2
        self.user = self.user2
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        # Let's check the current number of friend requests
        numInvitationsBefore = Invitation.objects.count()

        # user2 wants to send a friend request to user1. But they are already friends.
        data = {"token":self.token.key, "username": "user1"}
        
        with self.assertRaisesMessage(ValueError, 'You are already friends'):
            response = self.client.post(reverse('send_invitation'), data=json.dumps(data), content_type='application/json')

        # Let's see that nothing has changed 
        numInvitationsAfter = Invitation.objects.count()
        self.assertEqual(numInvitationsBefore, numInvitationsAfter)
        
        #------------------------------------------------------------------------------------------

        # Wee log in as user4
        self.user = self.user4
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        # Let's check the current number of friend requests
        numInvitationsBefore = Invitation.objects.count()

        # User4 wants to send a friend request to user5.
        data = {"token":self.token.key, "username": "user5"}
        response = self.client.post(reverse('send_invitation'), data=json.dumps(data), content_type='application/json')

        # Let's check the status of the HTTP request.
        self.assertEqual(200, response.status_code)

        # We see that a new friend request has been added.
        numInvitationsAfter = Invitation.objects.count()
        self.assertEqual(numInvitationsBefore+1, numInvitationsAfter)


    def test_accept_friend(self):
        """ The method 'accept_friend' is used to accept a friend request sent from another user."""
        
        # We log in as user2
        self.user = self.user2
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        data = {"token":self.token.key, "sendername": "user4"}
        # user2 was the one who sent the friend request to user4. user2 should not be able to accept the request.
        
        # Let's check the current status of the request
        statusBefore = Invitation.objects.get(pk=2).status
        self.assertEqual(statusBefore, 'P')
        

        with self.assertRaisesMessage(ValueError, "There is no pending invitation for that two users"):
            response = self.client.post(reverse('accept_friend'), data=json.dumps(data), content_type='application/json')

        # We see that the status hasn't changed
        statusAfter = Invitation.objects.get(pk=2).status
        self.assertEqual(statusAfter, 'P')

        #------------------------------------------------------------------------------------------

        #We log in as user1
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        data = {"token":self.token.key, "sendername": "user5"}
        #user5 has sent a friend request to user1. Now, user1 should be able to accept it.

        statusBefore = Invitation.objects.get(pk=4).status
        self.assertEqual(statusBefore, 'P')

        response = self.client.post(reverse('accept_friend'), data=json.dumps(data), content_type='application/json')
       
        self.assertEqual(200, response.status_code)

        # We see that the friend request now has an "ACCEPTED" status
        statusAfter = Invitation.objects.get(pk=4).status
        self.assertEqual(statusAfter, 'A')



    def test_reject_friend(self):
        """ The method 'reject_friend' is used to reject a friend request sent from another user."""
        
        # We log in as user2
        self.user = self.user2
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        data = {"token":self.token.key, "sendername": "user1"}
        # user2 has already acceped the friend request from user1. Once accepted, it cannot be rejected.
        
        # Let's check the current status of the request
        statusBefore = Invitation.objects.get(pk=1).status
        self.assertEqual(statusBefore, 'A')

        with self.assertRaisesMessage(ValueError, "There is no pending invitation for that two users"):
            response = self.client.post(reverse('reject_friend'), data=json.dumps(data), content_type='application/json')

        # We see that the status hasn't changed
        statusAfter = Invitation.objects.get(pk=1).status
        self.assertEqual(statusAfter, 'A')

        #------------------------------------------------------------------------------------------

        # We log in as user1
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        data = {"token":self.token.key, "sendername": "user5"}
        #user5 has sent a friend request to user1. Now, user1 should be able to reject it.

        # Let's check the current status of the request
        statusBefore = Invitation.objects.get(pk=4).status
        self.assertEqual(statusBefore, 'P')

        response = self.client.post(reverse('reject_friend'), data=json.dumps(data), content_type='application/json')
       
        self.assertEqual(200, response.status_code)

        # We see that the status of the friend request is now 'REJECTED'.
        statusAfter = Invitation.objects.get(pk=4).status
        self.assertEqual(statusAfter, 'R')


       
    def test_rate_user(self):
        """The method 'rate_user' makes it possible for a user to rate a friend of his/hers"""

        #We log in as user2
        self.user = self.user2
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # user2 and user4 are not friends yet. The application have a PENDING status. Therefore, user2 cannot rate user4.
        data = {"rating": "1", "voted": "user4"}

        # This is the total number of rates:
        numRatesBefore = Rate.objects.count()

        # And this is the rating of user4
        self.assertTrue(UserProfile.objects.get(pk=4).numRate == 1)
        self.assertTrue(UserProfile.objects.get(pk=4).avarageRate == 2)

        with self.assertRaisesMessage(ValueError, "You can not rate this user"):
            response = self.client.post(reverse('rate_user'), data=json.dumps(data), content_type='application/json')
       
        # We check that nothing has changed
        numRatesAfter = Rate.objects.count()
        self.assertEqual(numRatesBefore, numRatesAfter)
        self.assertTrue(UserProfile.objects.get(pk=4).numRate == 1)
        self.assertTrue(UserProfile.objects.get(pk=4).avarageRate == 2)
       

        #------------------------------------------------------------------------------------------

        # We log in as user3       
        self.user = self.user3
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # user3 wants to rate user2. They are friends. users3 hasn't voted user2 yet.
        data = {"rating": "5", "voted": "user2"}

        # This is the the total number of rates:
        numRatesBefore = Rate.objects.count()

        # user2 has only one rate
        self.assertTrue(UserProfile.objects.get(pk=2).numRate == 1)
        # user2 has a rating of 3
        self.assertTrue(UserProfile.objects.get(pk=2).avarageRate == 3)


        response = self.client.post(reverse('rate_user'), data=json.dumps(data), content_type='application/json')       
        self.assertEqual(200, response.status_code)

        # There is a new vote
        numRatesAfter = Rate.objects.count()
        self.assertEqual(numRatesBefore+1, numRatesAfter)

        # user2 now has 2 rates
        self.assertTrue(UserProfile.objects.get(pk=2).numRate == 2)

        #The rating has been updated successfully
        self.assertTrue(UserProfile.objects.get(pk=2).avarageRate == 4)


        #------------------------------------------------------------------------------------------

        # We log in as user1
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # user1 has already rated user4. But user1 wants to change his/her vote.
        data = {"rating": "4", "voted": "user4"}


        # This is the the total number of rates:
        numRatesBefore = Rate.objects.count()

        # This is the number of rates and the average rating of user4
        self.assertTrue(UserProfile.objects.get(pk=4).numRate == 1)
        self.assertTrue(UserProfile.objects.get(pk=4).avarageRate == 2)

        response = self.client.post(reverse('rate_user'), data=json.dumps(data), content_type='application/json')
       
        self.assertEqual(200, response.status_code)

        # We see that the number of rates remains the same
        numRatesAfter = Rate.objects.count()
        self.assertEqual(numRatesBefore, numRatesAfter)

        # user4 still has only 1 rate
        self.assertTrue(UserProfile.objects.get(pk=4).numRate == 1)

        # But his/her average rating has been updated
        self.assertTrue(UserProfile.objects.get(pk=4).avarageRate == 4)

    def test_list_languages(self):
        """The method 'listLanguages' has to return a list with all laguages."""

        # We log in as 'user1'
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        response = self.client.get(reverse('list_languages'))

        # We check the status code of the request
        self.assertEqual(200, response.status_code)

        # user1 has salected 2 languages. Let's check this:
        jsonResponse = response.json()
    
        self.assertTrue(len(jsonResponse) == 5)
           

    def test_list_cities(self):
        """The method 'listCities' has to return a list with all cities."""

        # We log in as 'user1'
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        response = self.client.get(reverse('list_cities'))

        # We check the status code of the request
        self.assertEqual(200, response.status_code)

        # There are 6 cities on the system. Let's check this:
        jsonResponse = response.json()

        self.assertTrue(len(jsonResponse) == 6)

    
       # We log in as 'user2'
        self.user = self.user2
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        response = self.client.get(reverse('list_cities'))

        # We check the status code of the request
        self.assertEqual(200, response.status_code)

        # There are 6 cities on the system. Let's check this:
        jsonResponse = response.json()
        self.assertTrue(len(jsonResponse) == 6)

    def test_list_interest(self):
        """The method 'listInterest' has to return a list with all the interests."""

        # We log in as 'user1'
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        response = self.client.get(reverse('list_interest'))

        # We check the status code of the request
        self.assertEqual(200, response.status_code)

        # There are 8 interest on the system. Let's check this:
        jsonResponse = response.json()
        self.assertTrue(len(jsonResponse) == 8)

    
       # We log in as 'user2'
        self.user = self.user2
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        response = self.client.get(reverse('list_interest'))

        # We check the status code of the request
        self.assertEqual(200, response.status_code)

        # There are 8 interest on the system. Let's check this:
        jsonResponse = response.json()
        self.assertTrue(len(jsonResponse) == 8)

    def test_get_friends(self):
        """The method 'getFriends' has to return a list with all the users with a invitation acepted by the 2 users."""

        # We log in as user1
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # We are still logged as user1
        data = {"token":self.token.key}

        # user 1 have an accepted invitation with the user 2 and other with the user 4
        response = self.client.post(reverse('get_friends'), data, format='json')
       
        self.assertEqual(200, response.status_code)

        jsonResponse = response.json()
        #Check that there are 2 friends
        self.assertTrue(len(jsonResponse)== 2)
        
        #Check they are user2 and user4
        self.assertEqual(jsonResponse[0]['user']['id'], self.user2.id)
        self.assertEqual(jsonResponse[1]['user']['id'], self.user4.id)

    def test_get_pending(self):
        """The method 'getPending' has to return a list with all the users with a invitation pending by the 2 users."""

        # We log in as user1
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # We are still logged as user1
        data = {"token":self.token.key}

        # user 1 have an pending invitation with the user 5
        response = self.client.post(reverse('get_pending'), data, format='json')
       
        self.assertEqual(200, response.status_code)

        jsonResponse = response.json()
        #Check that there are 1 pendings
        self.assertTrue(len(jsonResponse)== 1)
        
        #Check he is user5
        self.assertEqual(jsonResponse[0]['user']['id'], self.user5.id)
  
  

    def test_create_trip(self):
        """The method 'createTrip' allows users to create their own trips"""
      
        # We log in as user1
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        #Let's check the current number of trips
        numTripsBefore = Trip.objects.count()

        # This is the trip we want to create. We add two cities to the trip - city1 and city2
        cities = []
        cities.append(1)
        cities.append(2)
        cities = json.dumps(cities)
        
        data = {
        "user_id": "1" , 
        "title": "trip13", 
        "description": "trip13 description", 
        "price": 7200, 
        "start_date": "2019-05-24", 
        "end_date": "2019-05-31", 
        "tripType": "PUBLIC", 
        "cities": cities,
        "file": ""
        }

        response = self.client.post(reverse('create_trip'), data, format='json')
       
        # Let's check the HTTP status of the response
        self.assertEqual(200, response.status_code)

        #Let's check the number of trips now
        numTripsAfter = Trip.objects.count()

        #A new trip was created
        self.assertEqual(numTripsBefore+1, numTripsAfter)

        #Let's check that the new trip really has 2 cities
        self.assertTrue(Trip.objects.get(pk=13).cities.count() == 2)

       


    def test_get_trip(self):
        """The method 'get_trip' has to return a trip selected by the current user."""

        # We log in as 'user1'
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        response = self.client.get('/getTrip/1/')

        # We check the status code of the request
        self.assertEqual(200, response.status_code)

        # There are 1 trip selected. Let's check this:
        jsonResponse = response.json()

        trip=self.trip1
        serializer = TripSerializer(trip, many=False)

        self.assertEqual(jsonResponse['trip'], serializer.data)


    def test_edit_trip(self):
        """The method 'createTrip' allows users to create their own trips"""
      
        # We log in as user1
        self.user = self.user2
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        

        # This is the trip we want to create. We add two cities to the trip - city1 and city2
        cities = []
        cities.append(1)
        cities.append(2)
        cities = json.dumps(cities)
        
        data = {
        "token":self.token.key, 
        "tripId":4,
        "user_id": "2" , 
        "title": "editedTrip", 
        "file": "trip/default_trip.jpg",
        "description": "edited trip13 description", 
        "price": 7200, 
        "startDate": datetime.date(2019, 5, 1), 
        "endDate": datetime.date(2019, 5, 31), 
        "tripType": "PUBLIC", 
        "cities": cities,
        }
        
            
        # Let's check the current name of the title trip
        self.assertEqual(self.trip4.title, 'trip4')

        response = self.client.post(reverse('edit_trip'), data, format='json')
       
        # Let's check the HTTP status of the response
        self.assertEqual(201, response.status_code)
        
        # Let's see how the title has been changed
        self.assertEqual(Trip.objects.get(pk=4).title, 'editedTrip')



    def test_register_user(self):
        """The method 'registerUser' is used to regist an user."""
      
        data = {"username": "user7", "status": "A" , "password": "user7", "email": "user7@gmail.com", "firstName": "user7", "lastName": "user7", "description": "user7 description", "birthdate": "1991-03-30", "gender": "M", "nationality": "spanish", "city": "Madrid", "profesion": "N/A","civilStatus": "M", "languages": {"english"}, "interests":{"cooking"}}

        response = self.client.post(reverse('register_user'), data, format='json')
       
        self.assertEqual(201, response.status_code)
        #The user has been registed.
        self.assertEqual(UserProfile.objects.get(pk=7).user.username, 'user7')  



    def test_set_user_to_premium(self):
        """The method 'setUserToPremium' is used to make premium the users than have paid the premium."""
        
        # We log in as user1
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
     
        data = {"token":self.token.key, "user": "user1"}
        # Let's check the current status of the premium
        statusBefore = UserProfile.objects.get(pk=1).isPremium
        self.assertEqual(statusBefore, False)

        response = self.client.post(reverse('set_user_to_premium'), data, format='json')
       
        self.assertEqual(200, response.status_code)

        #The premium has been accepted.
        statusAfter = UserProfile.objects.get(pk=1).isPremium
        self.assertEqual(statusAfter, True)

    def test_get_user(self):
        """The method 'getUser' is used response with an user by a token."""
        # We log in as user1
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # We are still logged as user1
        data = {"token":self.token.key}

        # Will ask for user 1 
        response = self.client.post(reverse('get_user'), data, format='json')
        self.assertEqual(200, response.status_code)

        jsonResponse = response.json()

        #Check that we get user1 
        self.assertEqual(jsonResponse['user']['id'], self.user1.id)
      #-------------------------------------------------------------
      # We log in as user2
        self.user = self.user2
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # We are still logged as user1
        data = {"token":self.token.key}

        # Will ask for user2 
        response = self.client.post(reverse('get_user'), data, format='json')
        self.assertEqual(200, response.status_code)

        jsonResponse = response.json()

        #Check that we get user2 
        self.assertEqual(jsonResponse['user']['id'], self.user2.id)
    
    def test_get_user_by_id(self):
        """The method 'getUser' is used response with an user by a id."""

        # We log in as user1
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # We are still logged as user1
        data = {"user_id": '2'}

        # Will ask for user 2 
        response = self.client.post(reverse('get_user_by_id'), data, format='json')
        self.assertEqual(200, response.status_code)

        jsonResponse = response.json()

        #Check that we get user2 
        self.assertEqual(jsonResponse['user']['id'], self.user2.id)
        #----------------------------------------------------------------
        # We log in as user1
        # We are still logged as user3
        data = {"user_id": '3'}

        # Will ask for user 3 
        response = self.client.post(reverse('get_user_by_id'), data, format='json')
        self.assertEqual(200, response.status_code)

        jsonResponse = response.json()

        #Check that we get user3 
        self.assertEqual(jsonResponse['user']['id'], self.user3.id)

    def test_user_list(self):
        """The method 'userList' is used to get an user by his username."""

        # We log in as 'user1'
        self.user = self.user1
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
        response = self.client.get('/users/user1/')

        # We check the status code of the request
        self.assertEqual(200, response.status_code)

        # Should get the user1. Let's check this:
        jsonResponse = response.json()

        user=self.user1
        serializer = UserSerializer(user, many=False)

        self.assertEqual(jsonResponse['user'], serializer.data)

    
def test_get_discover_view(self):
        """The method 'getDiscover' has to return a list with all the users with a few of interest same of yours."""

        # We log in as user4
        self.user = self.user4
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # We are still logged as user4
        data = {"token":self.token.key, "limit": "0", "offset": "3"}
        response = self.client.post(reverse('get_discover'), data, format='json')
       
        self.assertEqual(200, response.status_code)

        # will response wiht users with ordered for the number of coincidences on trips, friends and interest. user2 and 4 have the more coincidences and dont have an Invitation on pending, accepted or rejected
        jsonResponse = response.json()
    
        # let's check it
        self.assertEqual(jsonResponse[0]['user']['username'], self.user2.username)

    
      