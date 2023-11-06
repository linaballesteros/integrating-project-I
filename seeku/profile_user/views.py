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
#Librerias para mandar correos automaticos
from dotenv import load_dotenv 
import os
from email.message import EmailMessage
import ssl
import smtplib
from utils.forms import ObjectForm, ClaimObject
from datetime import datetime
from firebase_admin import credentials, auth, firestore, initialize_app
from accounts.views import login_required

def get_user_data(request):
    user_uid = request.session.get('user_uid', None)
    user_ref = db.collection('usuario_eafit').document(user_uid)
    user_data = user_ref.get()
    user_dict = user_data.to_dict()
    return user_dict
#Connect to firebase data. 
#-------------------------------------------------------------------------------------------
config = {
  'apiKey': "AIzaSyB01Ld99k0bH5nGA2QSo1IDYWwOMLyC0gc",
  'authDomain': "seek-u-34bb1.firebaseapp.com",
  'databaseURL': "https://seek-u-34bb1-default-rtdb.firebaseio.com",
  'projectId': "seek-u-34bb1",
  'storageBucket': "seek-u-34bb1.appspot.com",
  'messagingSenderId': "160388318273",
  'appId': "1:160388318273:web:cfbcc3a6fe271119c4b2c0",
  'measurementId': "G-4PZTY17X6V"
}

cred = credentials.Certificate('seek-u-34bb1-firebase-adminsdk-qezx3-e8b002c1a6.json')


firebase = pyrebase.initialize_app(config)
db = firestore.client()


auth_pyrebase = firebase.auth()




@login_required
def my_profile(request):
    data = get_user_data(request)
    user_role = data['profile_role']
    user_uid = request.session.get('user_uid', None)
    if request.method == 'POST':
        # Limpiar la sesión de Django (eliminar el UID del usuario)
        del request.session['user_uid']

        log_out = reverse('home')  # Obtiene la URL de inicio de sesión basada en el nombre
        return redirect(log_out)  # Redirige al usuario a la página de inicio de sesión
    
    
    user_ref = db.collection('usuario_eafit').document(user_uid)
    # Obtiene los datos del usuario
    user_data = user_ref.get()
    user_dict = user_data.to_dict()
    return render(request, 'app\profile.html', {'user_data': user_dict, 'user_role': user_role})
  


@login_required
def edit_profile_view(request):
    data = get_user_data(request)
    user_role = data['profile_role']
    
    user_uid = request.session.get('user_uid', None)
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        
        user_ref = db.collection('usuario_eafit').document(user_uid)
        user_data = user_ref.get()
        user_dict = user_data.to_dict()
        print(user_dict)
        
        nuevos_valores = {
        'name': name,
        'email': email,
        'phone': phone,
        }
        
        user_ref.update(nuevos_valores)
        
    user_ref = db.collection('usuario_eafit').document(user_uid)
    # Obtiene los datos del usuario
    user_data = user_ref.get()
    user_dict = user_data.to_dict()
        
    return render(request, "app\edit_profile.html", {'user_data' : user_dict, 'user_role': user_role})

