from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

class Venue(models.Model):
    name = models.CharField("Venue name", max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip code', max_length=15)
    phone = models.CharField('contactphone', max_length=25)
    web = models.URLField('Website Adress' )
    email_address = models.EmailField('Email address', blank=True)

    def __str__(self):
        return self.name

class myClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField('Event name', max_length=120)
    event_date= models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    #venue = models.CharField(max_length=120)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(myClubUser, blank=True) # Aqui é uma chave muitos para muitos

    def __str__(self):
        return self.name

