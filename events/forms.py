from tkinter import Widget
from django import forms
from django.forms import ModelForm
from .models import Venue, Event

#Criacao do fomulario do Venue

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        #fields = "__all__" #Dessa forma pega todos os campos
        fields = ('name', 'address','zip_code','phone', 'web', 'email_address') #Nesse aqui voce escolhe os campos q quer q apareça

        #Nessa parte aqui vc configura a label que vc deseja
        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
        }

        #Essa é a parte onde se pode colocar uma classe nas tags ou outras coisas
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Venue Name'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Address'}),
            'zip_code': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Zip Code'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Phone'}),
            'web': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Web'}),
            'email_address': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}),
        }

#Criacao do fomulario de Eventos

class EventForm(ModelForm):
    class Meta:
        model = Event
        #fields = "__all__" #Dessa forma pega todos os campos
        fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description') #Nesse aqui voce escolhe os campos q quer q apareça

        #Nessa parte aqui vc configura a label que vc deseja
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'venue': 'Venue',
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': '',
        }

        #Essa é a parte onde se pode colocar uma classe nas tags ou outras coisas
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event Date'}),
            'venue': forms.Select(attrs={'class':'form-select', 'placeholder': 'Venue'}),
            'manager': forms.Select(attrs={'class':'form-select', 'placeholder': 'Manager'}),
            'attendees': forms.SelectMultiple(attrs={'class':'form-select', 'placeholder': 'Attendees'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Description'}),

        }