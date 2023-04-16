from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

SKYDIVE_TYPE = (
    ('tandemskydive', 'Tandem Skydive',),
    ('learnskydive', 'Learn Skydive',),
    ('licenseskydive', 'Licensed Skydive',)
)

CURR_TYPE = (
    ('cad', 'CAD',),
    ('inr', 'INR',),
    ('usa', 'USA',),
)

STATUS = (
    ('confirmed', 'CONFIRMED'),
    ('cancelled', 'CANCELLED'),
)


class Destination(models.Model):
    id = models.IntegerField(primary_key=True)
    province = models.CharField(max_length=20)
    img = models.ImageField(upload_to='pics')
    number = models.IntegerField(default=50)

    def __str__(self):
        return self.province


class Destination_desc(models.Model):
    dest_id = models.AutoField(primary_key=True)
    province = models.CharField(max_length=20)
    price = models.IntegerField(default=2000)
    rating = models.IntegerField(default=5)
    desc = models.TextField()
    img_destin = models.ImageField(upload_to='pics')
    type_skydive = models.CharField(max_length=50, choices=SKYDIVE_TYPE)
    curr = models.CharField(max_length=10, choices=CURR_TYPE, default='cad')

    def __str__(self):
        return self.province + "-" + self.type_skydive


class Passenger(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(default=18)


class Cards(models.Model):
    Card_number = models.CharField(primary_key=True, max_length=16)
    Ex_month = models.CharField(max_length=2)
    Ex_Year = models.CharField(max_length=2)
    CVV = models.CharField(max_length=3)
    Balance = models.CharField(max_length=8)


class Transactions(models.Model):
    Transactions_ID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10)
    Amount = models.CharField(max_length=8)
    Status = models.CharField(default="Failed", max_length=15)
    Payment_method = models.CharField(blank=True, max_length=15)
    Date_Time = models.CharField(default=datetime.now, max_length=19)


class Reservation(models.Model):
    """ Reservation representing single date and total/available spots for day """
    date_available = models.DateField(null=False, blank=False)
    spots_total = models.IntegerField(null=True, default=50)
    spots_free = models.IntegerField(null=True, default=50)
    destination = models.ForeignKey(Destination, related_name="destin", on_delete=models.CASCADE)
    type_skydive = models.CharField(max_length=50, choices=SKYDIVE_TYPE, default='tandemskydive')

    def __str__(self):
        return str(self.date_available) + "Total:" + str(self.spots_total) + "Free:" + str(self.spots_free)


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings", blank=True, null=True)
    passengers = models.ManyToManyField(Passenger, related_name="skydive_tickets")
    booking_date = models.DateField(default=datetime.now, blank=True, null=True)
    total_fare = models.FloatField(blank=True, null=True)
    type_skydive = models.CharField(max_length=50, choices=SKYDIVE_TYPE)
    destination_desc = models.ForeignKey(Destination_desc, related_name="dest", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default='cancelled')

    def __str__(self):
        return str(self.booking_id)


class NetBanking(models.Model):
    Username = models.CharField(primary_key=True, max_length=16)
    Password = models.CharField(max_length=14)
    Bank = models.CharField(max_length=25)
    Balance = models.CharField(max_length=9)


class Applicant(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    resume = models.FileField(upload_to="applicants/resume/", null=True, default=None)
    cover_letter = models.FileField(upload_to="applicants/cover_letter/", null=True, default=None)
    comments = models.TextField(blank=True)

    def __str__(self):
        return self.email


class Subscriber(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
