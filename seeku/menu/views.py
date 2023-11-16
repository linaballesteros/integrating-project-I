#Librerias para manejar firebase, son firebase_admin y pyrebase
from django.shortcuts import render
import folium # map library
import webbrowser
from folium.plugins import MarkerCluster # markers
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models import F
from django.db.models import Value
from django.db.models import CharField
from django.views.generic import View
import pyrebase
from django.shortcuts import redirect
from django.contrib import messages
from firebase_admin._auth_utils import handle_auth_backend_error
from django.urls import reverse
from app.models import Object
from django.shortcuts import render, get_object_or_404
from django.db.models import Q # para hacer consultas
from django.http import HttpResponse
from functools import wraps
import webbrowser
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
#Librerias para mandar correos automaticos
from dotenv import load_dotenv 
import os
from email.message import EmailMessage
import ssl
import smtplib
from utils.forms import ObjectForm, ClaimObject
from datetime import datetime
from profile_user.views import get_user_data


def home(request):

    data = get_user_data(request)
    print(data)
    if data is not None:
        user_role = data['profile_role']
        print(user_role)
    else:
        print("holi")
        user_role = 'guest'
    searchTerm = request.GET.get('searchObject')
    objects_complaints = Object.objects.filter(complaints_amount__gt=2)
    
    if searchTerm and user_role != 'guest':
        objects = Object.objects.filter(title__icontains=searchTerm)        
    elif searchTerm == False:
        objects = Object.objects.all()
    
    else:
        return render(request, "index.html", {'user_role': user_role})   
    
    
    return render(request, "index2.html", {'user_role': user_role, 'searchTerm': searchTerm, 'objects': objects, 'objects_complaints': objects_complaints}) 


def index_es(request):
    data = get_user_data(request)
    if data is not None:
        user_role = data['profile_role']
    else:
        user_role = 'guest'
    searchTerm = request.GET.get('searchObject')
    objects_complaints = Object.objects.filter(complaints_amount__gt=2)
    
    if searchTerm and user_role != 'guest':
        objects = Object.objects.filter(title__icontains=searchTerm)        
    elif searchTerm == False:
        objects = Object.objects.all()
    else:
        return render(request, "index_es.html")   
    

    return render(request, "index2_es.html", {'user_role': user_role, 'searchTerm': searchTerm, 'objects': objects, 'objects_complaints': objects_complaints}) 

def about(request):
    data = get_user_data(request)
    if data is not None:
        user_role = data['profile_role']
    else:
        user_role = 'student'
    objects_complaints = Object.objects.filter(complaints_amount__gt=2)
    return render(request, "_about.html", {'user_role': user_role, 'objects_complaints': objects_complaints})


def about_es(request):
    data = get_user_data(request)
    if data is not None:
        user_role = data['profile_role']
    else:
        user_role = 'guest'
    objects_complaints = Object.objects.filter(complaints_amount__gt=2)
    return render(request, "_about_es.html", {'user_role': user_role, 'objects_complaints': objects_complaints})