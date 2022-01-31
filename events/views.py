from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event

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

def all_events(request):

    event_list = Event.objects.all()

    context = {
        "event_list": event_list
    }

    return render(request, 'events/events.html', context)
