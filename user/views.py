from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()
        login(request,newUser)
        messages.success(request,"Muveffeqiyyetle qeydiyyatdan kecdiniz")
        return redirect("index")
    context = {
        "form" : form
    }
    return render(request,"register.html", context)
    
def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        if user is None:
            messages.info(request, "Istifadeci adi ve ya shifre yanlishdir")
            return render(request, "login.html", context)
        messages.success(request, "Daxil ola bildin")
        login(request, user)
        return redirect("index")
    return render(request,"login.html",context)

@login_required(login_url = "user:login")
def logoutUser(request):
    logout(request)
    messages.success(request,"Sistemden cixdin")
    return redirect("index")