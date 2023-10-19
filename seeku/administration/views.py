from django.shortcuts import render
#Helps that the app work
from django.shortcuts import render
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models import F
from django.db.models import Value
from django.db.models import CharField
from django.views.generic import View
from firebase_admin import credentials, auth, firestore, initialize_app
import pyrebase
from django.shortcuts import redirect
from django.contrib import messages
from firebase_admin._auth_utils import handle_auth_backend_error
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q # para hacer consultas
from django.http import HttpResponse
from functools import wraps
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
#Send emails :)
from dotenv import load_dotenv 
import os
from email.message import EmailMessage
import ssl
import smtplib
from datetime import datetime
# Connect with the utils and app
from app.models import Object
from utils.choises import CATEGORY_CHOICES, HOUR_CHOICES, COLOR_CHOICES, BLOCK_CHOICES, OFFICE_CHOICES, STATUS_CHOICES, RECOVERED_CHOICES
from utils.forms import ObjectForm, ClaimObject



#View to publish the object with the security.
def publish_object(request):
    return render(request, "app\publish_object.html")


#Function to publish the object. 
def publish_object_(request): # for publishing objects (vista vigilantes)
    if request.method == 'POST':
        form = ObjectForm(request.POST, request.FILES)
        print("posttt")
        if form.is_valid():
            new_object = form.save()  # Save the form data to the database
            print(form.errors)
            print("pasó el valid")
        else:
            print(form.errors)  
    else:
        form = ObjectForm()

    return render(request, 'app\publish_object.html', {'form': form})



#Function to edit the object by the security. 
def edit_object(request, object_id): # UPDATE OBJECT
    object_to_edit = get_object_or_404(Object, pk=object_id)
    if request.method == "POST" and 'save_changes' in request.POST:
        print("holiss")
        title = request.POST.get('title')
        color = request.POST.get('color')
        image = request.FILES.get('image')  
        date_found = request.POST.get('date_found')
        brands = request.POST.get('brands')
        place_found = request.POST.get('place_found')
        hour_range = request.POST.get('hour_range')
        description = request.POST.get('description')
        category = request.POST.getlist('category')  
        
        # updating data of objects in django admin
        object_to_edit.title = title
        object_to_edit.color = color
        
        if image:
            object_to_edit.image = image
            
        object_to_edit.date_found = date_found
        object_to_edit.brands = brands
        object_to_edit.place_found = place_found
        object_to_edit.hour_range = hour_range
        object_to_edit.description = description
        object_to_edit.category = category 
        
        
        object_to_edit.save() # changes
        return render(request, 'edit_object.html', {'object_to_edit' : object_to_edit})
    elif request.method == "POST" and 'delete_object' in request.POST:
         obj_to_delete = get_object_or_404(Object, pk=object_id)
         obj_to_delete.delete()
         return render(request, 'app\my_objects.html', {'object_to_edit' : object_to_edit})   
    else:
        form = ObjectForm()
        return render(request, 'app\edit_object.html', {'object_to_edit' : object_to_edit})

#Function that edit the object to the security
def delete_object(request, object_id):
    obj_to_delete = get_object_or_404(Object, pk=object_id)
    if request.method == "GET":
        print("gettt")
        obj_to_delete.delete()
    return render(request, 'app\my_objects.html')

def  my_objects(request):
    objects = Object.objects.all()  # Retrieve all objects from the database
    return render(request, 'app\my_objects.html', {'objects': objects})


