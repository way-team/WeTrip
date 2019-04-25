from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Language(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # A user profile has:
    #   Username
    #   Password
    #   First name
    #   Last name
    #   Description
    #   Birthdate
    #   Gender
    #   Nationality
    #   City
    #   Photo
    #   Status
    #   AvarageRate
    #   NumRate
    #   IsPremium
    #   IsSuperUser
    languages = models.ManyToManyField("Language")
    email = models.EmailField(null=False, default='')
    first_name = models.CharField(max_length=30, blank=False, default='')
    last_name = models.CharField(max_length=60, blank=False, default='')
    description = models.CharField(max_length=200, blank=True)
    birthdate = models.DateField(default="1999-12-01")
    city = models.CharField(max_length=80, null=True)
    nationality = models.CharField(max_length=40, blank=False, default='')
    photo = models.ImageField(
        default='user/profile/default.jpg', upload_to='user/profile')
    discoverPhoto = models.ImageField(
        default='user/discover/d_default.jpg', upload_to='user/discover')
    avarageRate = models.IntegerField(blank=False, default=0)
    numRate = models.IntegerField(blank=False, default=0)
    isPremium = models.BooleanField(default=False)
    datePremium = models.DateField(default="2019-04-09")

    STATUS_OPTIONS = (
        ('A', 'Active'),
        ('D', 'Delete'),
    )

    status = models.CharField(max_length=10, blank=False, default='')

    GENDER_OPTIONS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Non-binary'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_OPTIONS, null=True)

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def age(self):
        today = date.today()
        age = today - self.birthdate
        return age.year


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp', )


class Interest(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(
        UserProfile, related_name="interests", blank=True)

    def __str__(self):
        return self.name


class Invitation(models.Model):
    sender = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='invitationSender')
    receiver = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='invitationReceiver')

    STATUS_OPTIONS = (
        ('P', 'Pending'),
        ('R', 'Rejected'),
        ('A', 'Accepted'),
    )

    status = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.status


class Rate(models.Model):
    voter = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='voter')
    voted = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='voted')

    value = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(5)])

    def __str__(self):
        return self.value


class Global(models.Model):
    paypalEmail = models.EmailField(unique=True)
    premiumPrice = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "%s %d" % (self.paypalEmail, self.premiumPrice)


class Advertisement(models.Model):
    url = models.URLField()
    globalData = models.ForeignKey(
        "Global",
        default=1,
        on_delete=models.CASCADE,
        related_name='globalData')

    def __str__(self):
        return self.url


TRIPTYPE_CHOICES = [('PRIVATE', 'Private'), ('PUBLIC', 'Public')]


class Trip(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250, null=True, blank=True)
    startDate = models.DateField(default="1999-12-01")
    endDate = models.DateField(default="1999-12-01")
    tripType = models.CharField(
        max_length=7, choices=TRIPTYPE_CHOICES, default='Public')
    image = models.URLField(blank=True)
    status = models.BooleanField(default=True)
    userImage = models.ImageField(
        null=True, default='trip/default_trip.jpg', upload_to='trip')

    def __str__(self):
        return self.title


class Country(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey("Country", on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    trips = models.ManyToManyField(Trip, blank=True, related_name="cities")

    def __str__(self):
        return self.name


class Application(models.Model):
    applicant = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='applicant')
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name='applications')

    STATUS_OPTIONS = (
        ('P', 'Pending'),
        ('R', 'Rejected'),
        ('A', 'Accepted'),
    )

    status = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.status