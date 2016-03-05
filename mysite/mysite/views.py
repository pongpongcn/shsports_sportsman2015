from django.shortcuts import render
from django.contrib.auth import views as auth_views

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    return auth_views.login(request)

def logout(request):   
    return auth_views.logout_then_login(request)