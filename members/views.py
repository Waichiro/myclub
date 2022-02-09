from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationForm

#Aqui é a parte de login
def login_user(request):

    if request.method == "POST":
        username = request.POST['username'] #Ele pega o name do campo da tag la no html q tem esse msm nome 
        password = request.POST['password'] #Ele pega o name do campo da tag la no html q tem esse msm nome 
        user = authenticate(request, username=username, password=password) #Aqui ele faz a authenticacao para ver se existe e se ta tudo certo
        if user is not None: #Aqui se tiver algo escrito e tiver passado pela authenticacao ele vai fazer o login
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("There Was An Error Loggin In, Try Again...")) #Mensagem de erro caso o usuario nn exista ou esteja algo errado
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html')

#Aqui é a parte de logout
def logout_user(request):
    logout(request)#FAz o logout
    messages.success(request, ("You Were Logged Out!!"))#Mensagem indicando q fez o logout
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Successful!"))
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'authenticate/register_user.html', {"form":form})