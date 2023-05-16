from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User

# Create your views here.
def home(request):
    return render(request,'educationapp/home.html')

def login(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "educationapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "educationapp/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
 
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "educationapp/register.html", {
                "message": "Passwords must match!"
            })

        try:
            if username is "":
                return render(request, "educationapp/register.html",{
                    "message": "Username cannot be empty!"
                })
            user = User.objects.create_user(username, email, password)
            user.first_name=first_name
            user.last_name=last_name
            l=[user.first_name,user.last_name,user.password]
            for i in l:
                if i is "":
                    return render(request, "educationapp/register.html",{
                        "message": "All non-optional fields are compulsory!"
                    })
                else:
                    continue
            user.save()
        except IntegrityError:
            return render(request, "educationapp/register.html", {
                "message": "Username already taken!"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "educationapp/register.html")