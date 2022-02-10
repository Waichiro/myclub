from email import message
from multiprocessing import context
from django.shortcuts import redirect, render
import calendar
from django.contrib import messages
from calendar import HTMLCalendar
from django.http import HttpResponseRedirect
from datetime import datetime
from .models import Event, Venue
#import user model from django
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponse
import csv

#Nessa parte vai ficar todos os imports que precisa para gerar arquivos em PDF
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

#Aqui fica os imports para Pagination Stuff
from django.core.paginator import Paginator

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

    event_list = Event.objects.all().order_by('event_date')

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
            venue = form.save(commit=False)
            venue.owner = request.user.id #Quando a pessoa adicionar o venue ele vai colocar o id de quem ta criando como dono do Venue
            venue.save()
            #form.save()
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
    #venue_list = Venue.objects.all().order_by('name')#Puxa todos os dados q estao no banco de dados conforme a tabela
    venue_list = Venue.objects.all()

    #Set up pagination
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')
    venues = p.get_page(page)

    nums = "a" * venues.paginator.num_pages

    context = {
        "venue_list": venue_list,
        "venues": venues,
        "nums": nums
    }
    return render(request, 'events/venue.html', context)

#Nessa parte pega o id do banco de dados e assim so tras as informacoes contidas no id q foi pego
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id) #Ele pega somente a chave primaria q é o id do objeto na tabela
    venue_owner = User.objects.get(pk=venue.owner)
    context = {
        "venue": venue,
        "venue_owner": venue_owner
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
        #Nesse if abaixo ele fala q se o usuario for um super user ele pega o formulario
        # de super user, se nn for ele pega o formulario de usuario normal

        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')

        else:
            form = EventForm(request.POST)  
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user #Nessa parte ele adicionacomo manager do evento o usuario q criou
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')

    else:
        # Just goingo To The Page, Not Submitting
        if request.user.is_superuser:
            form = EventFormAdmin
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
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
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
    if request.user == event.manager: #Aqui ele vai ver se o usuario é dono do evento antes de excluir ele
        event.delete()
        messages.success(request, ("Event Delete With Success"))
        return redirect('list-events')#Redireciona para a lista de eventos
    else:
        messages.success(request, ("You aren't Authorized To Delete This Event"))
        return redirect('list-events')#Redireciona para a lista de eventos

#deleta um Venue
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id) #Ele pega somente a chave primaria q é o id do objeto na tabela  
    if request.user.id == venue.owner:# AQui ele comparar o id do usuario para ver se é igual o id do dono do Venue
        venue.delete()
        messages.success(request, ("Venue Delete With Success"))
        return redirect('list-venues')#Redireciona para a lista de venues
    else:
        messages.success(request, ("You aren't Authorized To Delete This Venue"))
        return redirect('list-venues')#Redireciona para a lista de venues


#Aqui gera um arquivo de texto em .txt
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    #Designa o modelo do banco de dados
    venues = Venue.objects.all()

    #Create blank list
    lines = []
    #loop pThu and output
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.phone}\n{venue.email_address}\n\n')


    #write textFile
    response.writelines(lines)
    return response 

#Aqui gera um arquivo de texto em .csv
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    #Designa o modelo do banco de dados
    venues = Venue.objects.all()

    #Create a csv writer
    writer = csv.writer(response)
  
    #Adiciona cabeçalhos de coluna ao arquiso csv
    writer.writerow(['Venue Name', 'Address', 'Phone', 'Email'])

    #loop pThu and output
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.phone, venue.email_address])


    return response 

#gera um arquivo em pdf dos venues
def venue_pdf(request):

    #Create bytestream buffer
    buf = io.BytesIO()

    #Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    #create a text objects
    textob = c.beginText()
    textob.setTextOrigin(inch, inch) 
    textob.setFont("Helvetica", 14)

    #Designa o modelo do banco de dados
    venues = Venue.objects.all()

    #Create a blank list
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.email_address)
        lines.append("  ")
        

    # Loop
    for line in lines:
        textob.textLine(line)

    #Finis Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    #return something
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')