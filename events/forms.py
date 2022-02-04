from tkinter import Widget
from django import forms
from django.forms import ModelForm
from .models import Venue

#Criacao do fomulario do Venue

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = "__all__" #Dessa forma pega todos os campos
        #fields = ('phone', 'web', 'email_address') #Nesse aqui voce escolhe os campos q quer q apareça

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