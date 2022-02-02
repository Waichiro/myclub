from django.contrib import admin

from .models import Venue, Event, myClubUser


admin.site.register(myClubUser)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone') #mostra apenas essas informaçoes
    ordering = ('-name',)#cria uma ordem por nome
    search_fields = ('name', 'address')# cria um campo de pesquisa 

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'manager')#ELe modifica os fildes conforme vc queira na area de admin
    list_display = ('name', 'event_date', 'venue') 
    list_filter = ('event_date', 'venue')#Adiciona um filtro ao lado
    ordering = ('-event_date', )