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
# Create your views here.


def home(request):
    searchTerm = request.GET.get('searchObject')
    if searchTerm:
        objects = Object.objects.filter(title__icontains=searchTerm)        
    elif searchTerm == False:
        objects = Object.objects.all()
    else:
        return render(request, "app\index.html")        
    return render(request, "app\index2.html", {'searchTerm': searchTerm, 'objects': objects}) 

def about(request):
    return render(request, "app\_about.html")