from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Venue(models.Model):
    name = models.CharField("Venue Name", max_length=40)
    address = models.CharField(max_length=40)
    zip_code = models.CharField("Zip Code", max_length=15)
    phone = models.CharField("Contact Phone", max_length=10, blank=True) # if the field is black so it's ok - not mandatory field
    web = models.URLField("Website Address")
    email_address = models.EmailField("Email", blank=True)

    def __str__(self):
        return self.name


class MyClubUser(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email_address = models.EmailField("User Email")

    def __str__(self):
        return self.first_name +" "+ self.last_name


class Event(models.Model):
    name = models.CharField("Event Name", max_length=40)
    event_date = models.DateTimeField("Event Date")
    venue = models.ForeignKey(Venue, blank=True, null=True ,on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)  # If the manager delete his acount set the manager name to null
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True)

    def __str__(self):
        return self.name


