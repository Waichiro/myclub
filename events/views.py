from multiprocessing import context
from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from django.http import HttpResponseRedirect
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm

#Aqui é o home do projeto onde fica o calendario
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    #deixa a primeira letra maiuscula
    month = month.capitalize()

    #Conversao de string do mes para inteiro
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    #Criacao do Calendario
    cal = HTMLCalendar().formatmonth(year, month_number)

    #Pega a data atual
    now = datetime.now()
    current_year = now.year

    #Pega a hora atual
    time = now.strftime('%I:%M %p') #formato do horario: 07:32 AM
    #time = now.strftime('%H:%M:%S') #formato do horario: 17:42:55

    context = {
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time
    }

    return render(request, 'events/home.html', context)

#Pega todos os eventos q estao no Banco de dados e lista eles
def all_events(request):

    event_list = Event.objects.all()

    context = {
        "event_list": event_list
    }

    return render(request, 'events/events.html', context)

#adiciona uma nova venue no banco de dados
def add_venue(request):
    submitted =  False

    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')

    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    context = {
        "form": form,
        "submitted": submitted
    }
    return render(request, 'events/add_venue.html', context)

#lista todas as venues no banco de dados
def list_venues(request):
    venue_list = Venue.objects.all()#Puxa todos os dados q estao no banco de dados conforme a tabela
    context = {
        "venue_list": venue_list
    }
    return render(request, 'events/venue.html', context)

#Nessa parte pega o id do banco de dados e assim so tras as informacoes contidas no id q foi pego
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id) #Ele pega somente a chave primaria q é o id do objeto na tabela
    context = {
        "venue": venue
    }
    return render(request, 'events/show_venue.html', context)

def search_venues(request):

    if request.method =="POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        context = {
            'searched': searched,
            'venues': venues
        }
        return render(request, 'events/search_venues.html', context)
    else:
        return render(request, 'events/search_venues.html', {})
#Aqui é a view para dar update na venue   
def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id) #Ele pega somente a chave primaria q é o id do objeto na tabela
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    context = {
        "venue": venue,
        "form": form
    }
    return render(request, 'events/update_venue.html', context)   

#Aqui fica a view para adicionar um novo evento
def add_event(request):
    submitted =  False

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')

    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    context = {
        "form": form,
        "submitted": submitted
    }
    return render(request, 'events/add_event.html', context)  

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id) #Ele pega somente a chave primaria q é o id do objeto na tabela
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    context = {
        "event": event,
        "form": form
    }
    return render(request, 'events/update_event.html', context)  

#deleta um evento
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id) #Ele pega somente a chave primaria q é o id do objeto na tabela  
    event.delete()
    return redirect('list-events')#Redireciona para a lista de eventos

#deleta um Venue
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id) #Ele pega somente a chave primaria q é o id do objeto na tabela  
    venue.delete()
    return redirect('list-venues')#Redireciona para a lista de venues