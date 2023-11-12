#Librerias para manejar firebase, son firebase_admin y pyrebase
from django.shortcuts import render
from datetime import datetime, timedelta, date

import folium # map library
import webbrowser
from django.utils import timezone
from folium.plugins import MarkerCluster # markers
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
from .models import Object, Noti
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
from .forms import ObjectForm, ClaimObject
from datetime import datetime
from accounts.views import login_required
from profile_user.views import get_user_data

#Connect to firebase data. 
#-------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

#Start de functions for the page. 



 
@login_required
def search(request):
    objects_complaints = Object.objects.filter(complaints_amount__gt=2)

    data = get_user_data(request)
    if data is not None:
        user_role = data['profile_role']
    else:
        user_role = 'guest'
    searchTerm = request.POST.get('searchObject')
    categories = request.POST.getlist('category')
    selected_blocks = request.POST.getlist('blockCheckboxes')
    start_date = request.POST.get('startDate')
    end_date = request.POST.get('endDate')
    start_hour = request.POST.get('startHour')
    end_hour = request.POST.get('endHour')
    
    objects = Object.objects.all()
    print("Selected Categories", categories)
    print("Search term =", searchTerm)
    
    if request.method == 'POST':
        
        if searchTerm == "salir":
            logout(request)
            return redirect('login')
        
        if searchTerm:
            objects = objects.filter(title__icontains=searchTerm)
        
        print("Selected Categories", categories)
        if categories:
            objects = objects.filter(category__in=categories)
            
        if categories and selected_blocks:
            objects = objects.filter(place_found__in=selected_blocks, category__in=categories)
            
        if categories and selected_blocks and start_date and end_date:
            try:

                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                
                # date range
                objects = objects.filter(place_found__in=selected_blocks, category__in=categories,date_found__gte=start_date, date_found__lte=end_date)
            except ValueError:
                print("Invalid date format")
                
        if categories and selected_blocks and start_date and end_date and start_hour and end_hour:
            try:

                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                start_hour = datetime.strptime(start_hour, '%H:%M').time()
                end_hour = datetime.strptime(end_hour, '%H:%M').time()
                
                # date range
                objects = objects.filter(place_found__in=selected_blocks, category__in=categories,date_found__gte=start_date, date_found__lte=end_date, hour_range__gte=start_hour,
                    hour_range__lte=end_hour)
            except ValueError:
                print("Invalid date format")
                
        print("Selected Blocks:", selected_blocks)
        
        
        
        print(start_date)
        print(end_date)

        if start_date and end_date:
            try:


                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                
                # date range
                objects = objects.filter(date_found__gte=start_date, date_found__lte=end_date)
            except ValueError:
                print("Invalid date format")
                
        if selected_blocks and start_date and end_date:
                try:

                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    
                    # 
                    objects = objects.filter(place_found__in=selected_blocks, date_found__gte=start_date, date_found__lte=end_date)
                except ValueError:
                    print("Invalid date format")
                
        else:
            print("Both start_date and end_date are required")
            
        if selected_blocks:
            objects = objects.filter(place_found__in=selected_blocks)
       # objects = objects.filter(date_found__gte=start_date, date_found__lte=end_date)
        if start_hour and end_hour and selected_blocks:
            try:
                # Convert the hour strings to time objects
                start_hour = datetime.strptime(start_hour, '%H:%M').time()
                end_hour = datetime.strptime(end_hour, '%H:%M').time()

                # Filter objects based on selected blocks and hour range
                objects = objects.filter(
                    place_found__in=selected_blocks,
                    hour_range__gte=start_hour,
                    hour_range__lte=end_hour
                )
            except ValueError:
                print("Invalid time format")
        else:
            print("Both start_hour and end_hour are required")
            
        if start_hour and end_hour and selected_blocks and start_date and end_date:
            try:
                # Convert the hour strings to time objects
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                start_hour = datetime.strptime(start_hour, '%H:%M').time()
                end_hour = datetime.strptime(end_hour, '%H:%M').time()

                # Filter objects based on selected blocks and hour range
                objects = objects.filter(
                    date_found__gte=start_date, 
                    date_found__lte=end_date,
                    place_found__in=selected_blocks,
                    hour_range__gte=start_hour,
                    hour_range__lte=end_hour
                )
            except ValueError:
                print("Invalid time format")
        else:
            print("Both start_hour and end_hour are required")
            
        if start_hour and end_hour:
            try:
                # Convert the hour strings to time objects
                start_hour = datetime.strptime(start_hour, '%H:%M').time()
                end_hour = datetime.strptime(end_hour, '%H:%M').time()

                # Filter objects based on selected blocks and hour range
                objects = objects.filter(
                    hour_range__gte=start_hour,
                    hour_range__lte=end_hour
                )
            except ValueError:
                print("Invalid time format")
        else:
            print("Both start_hour and end_hour are required")
        context = {
            'objects': objects,
            'searchTerm': '',  #
        }
   # selected_blocks = request.GET.getlist("blockCheckboxes")

    

    
   # if selected_blocks:
       # objects = objects.filter(place_found=selected_blocks)

    return render(request, "app\index2.html", {'searchTerm': searchTerm, 'objects': objects, 'user_role': user_role, 'objects_complaints': objects_complaints})

@login_required
def search_es(request):
    objects_complaints = Object.objects.filter(complaints_amount__gt=2)

    data = get_user_data(request)
    if data is not None:
        user_role = data['profile_role']
    else:
        user_role = 'guest'
    searchTerm = request.POST.get('searchObject')
    categories = request.POST.getlist('category')
    selected_blocks = request.POST.getlist('blockCheckboxes')
    start_date = request.POST.get('startDate')
    end_date = request.POST.get('endDate')
    start_hour = request.POST.get('startHour')
    end_hour = request.POST.get('endHour')
    
    objects = Object.objects.all()
    print("Selected Categories", categories)
    print("Search term =", searchTerm)
    
    if request.method == 'POST':
        
        if searchTerm == "salir":
            logout(request)
            return redirect('login')
        
        if searchTerm:
            objects = objects.filter(title__icontains=searchTerm)
        
        print("Selected Categories", categories)
        if categories:
            objects = objects.filter(category__in=categories)
            
        if categories and selected_blocks:
            objects = objects.filter(place_found__in=selected_blocks, category__in=categories)
            
        if categories and selected_blocks and start_date and end_date:
            try:

                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                
                # date range
                objects = objects.filter(place_found__in=selected_blocks, category__in=categories,date_found__gte=start_date, date_found__lte=end_date)
            except ValueError:
                print("Invalid date format")
                
        if categories and selected_blocks and start_date and end_date and start_hour and end_hour:
            try:

                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                start_hour = datetime.strptime(start_hour, '%H:%M').time()
                end_hour = datetime.strptime(end_hour, '%H:%M').time()
                
                # date range
                objects = objects.filter(place_found__in=selected_blocks, category__in=categories,date_found__gte=start_date, date_found__lte=end_date, hour_range__gte=start_hour,
                    hour_range__lte=end_hour)
            except ValueError:
                print("Invalid date format")
                
        print("Selected Blocks:", selected_blocks)
        
        
        
        print(start_date)
        print(end_date)

        if start_date and end_date:
            try:


                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                
                # date range
                objects = objects.filter(date_found__gte=start_date, date_found__lte=end_date)
            except ValueError:
                print("Invalid date format")
                
        if selected_blocks and start_date and end_date:
                try:

                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    
                    # 
                    objects = objects.filter(place_found__in=selected_blocks, date_found__gte=start_date, date_found__lte=end_date)
                except ValueError:
                    print("Invalid date format")
                
        else:
            print("Both start_date and end_date are required")
            
        if selected_blocks:
            objects = objects.filter(place_found__in=selected_blocks)
       # objects = objects.filter(date_found__gte=start_date, date_found__lte=end_date)
        if start_hour and end_hour and selected_blocks:
            try:
                # Convert the hour strings to time objects
                start_hour = datetime.strptime(start_hour, '%H:%M').time()
                end_hour = datetime.strptime(end_hour, '%H:%M').time()

                # Filter objects based on selected blocks and hour range
                objects = objects.filter(
                    place_found__in=selected_blocks,
                    hour_range__gte=start_hour,
                    hour_range__lte=end_hour
                )
            except ValueError:
                print("Invalid time format")
        else:
            print("Both start_hour and end_hour are required")
            
        if start_hour and end_hour and selected_blocks and start_date and end_date:
            try:
                # Convert the hour strings to time objects
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                start_hour = datetime.strptime(start_hour, '%H:%M').time()
                end_hour = datetime.strptime(end_hour, '%H:%M').time()

                # Filter objects based on selected blocks and hour range
                objects = objects.filter(
                    date_found__gte=start_date, 
                    date_found__lte=end_date,
                    place_found__in=selected_blocks,
                    hour_range__gte=start_hour,
                    hour_range__lte=end_hour
                )
            except ValueError:
                print("Invalid time format")
        else:
            print("Both start_hour and end_hour are required")
            
        if start_hour and end_hour:
            try:
                # Convert the hour strings to time objects
                start_hour = datetime.strptime(start_hour, '%H:%M').time()
                end_hour = datetime.strptime(end_hour, '%H:%M').time()

                # Filter objects based on selected blocks and hour range
                objects = objects.filter(
                    hour_range__gte=start_hour,
                    hour_range__lte=end_hour
                )
            except ValueError:
                print("Invalid time format")
        else:
            print("Both start_hour and end_hour are required")
        context = {
            'objects': objects,
            'searchTerm': '',  #
        }
   # selected_blocks = request.GET.getlist("blockCheckboxes")

    

    
   # if selected_blocks:
       # objects = objects.filter(place_found=selected_blocks)

    return render(request, "app\index2_es.html", {'searchTerm': searchTerm, 'objects': objects, 'user_role': user_role, 'objects_complaints': objects_complaints})

   
   
@login_required
def claim_request(request):

    data = get_user_data(request)
    if data is not None:
        user_role = data['profile_role']
    else:
        user_role = 'guest'
    return render(request, "app\claim_request.html", {'user_role': user_role})

@login_required
def history(request):
    objects_complaints = Object.objects.filter(complaints_amount__gt=2)

    data = get_user_data(request)
    if data is not None:
        user_role = data['profile_role']
    else:
        user_role = 'guest'
    print("entró a history")
    # Consulta la base de datos para obtener los objetos con object_status igual a "Claimed" para mostrarlos en el historial
    objetos_claimed = Object.objects.filter(object_status="Claimed")
    print(objetos_claimed)
    return render(request, 'app\history.html', {'objetos_claimed': objetos_claimed, 'user_role': user_role, 'objects_complaints': objects_complaints})

@login_required
def history_es(request):
    objects_complaints = Object.objects.filter(complaints_amount__gt=2)

    data = get_user_data(request)
    if data is not None:
        user_role = data['profile_role']
    else:
        user_role = 'guest'
    print("entró a history")
    # Consulta la base de datos para obtener los objetos con object_status igual a "Claimed" para mostrarlos en el historial
    objetos_claimed = Object.objects.filter(object_status="Claimed")
    print(objetos_claimed)
    return render(request, 'app\history_es.html', {'objetos_claimed': objetos_claimed, 'user_role': user_role, 'objects_complaints': objects_complaints})


# analytics


lost_object_names = [
    "Textbook: Calculus 101",
    "Student ID Card",
    "Laptop Charger",
    "Water Bottle: EAFIT Logo",
    "Notebook: Physics Lecture",
    "Umbrella: University Colors",
    "Graphing Calculator",
    "Headphones: Noise-Canceling",
    "Backpack: Laptop Compartment",
    "Library Book: History of Art",
    "Gym Bag: Sports Gear",
    "Cell Phone: iPhone X",
    "Lanyard: University Branded",
    "Glasses Case: Prescription",
    "Bike Helmet",
    "USB Flash Drive",
    "Scientific Calculator",
    "Textbook: Literature Classics",
    "Coffee Thermos: Stainless Steel",
    "Rain Boots: Campus Walks",
]

lost_object_brands = [
    "TextbookXpress",
    "StudentSecure",
    "TechPower Pro",
    "HydraQuench",
    "SmartNote",
    "ShelterShield",
    "MathMasters",
    "SoundScape",
    "UrbanCarry",
    "ReadAhead",
    "SportyGear",
    "iTech",
    "UniLanyard",
    "ClearSight",
    "RideSafe",
    "DataLink",
    "CalcGenius",
    "LitClassics",
    "ThermoMate",
    "RainStride",
]

BLOCK_CHOICES = [
    ('Block 1', 'Block 1'),
    ('Block 3', 'Block 3'),
    ('Block 4', 'Block 4'),
    ('Block 5', 'Block 5'),
    ('Block 6', 'Block 6'),
    ('Block 7', 'Block 7'),
    ('Block 8', 'Block 8'),
    ('Block 9', 'Block 9'),
    ('Block 10', 'Block 10'), 
    ('Block 12', 'Block 12'),
    ('Block 13', 'Block 13'),
    ('Block 14', 'Block 14'),
    ('Block 15', 'Block 15'),
    ('Block 16', 'Block 16'), 
    ('Block 17', 'Block 17'),
    ('Block 18', 'Block 18'),
    ('Block 19', 'Block 19'),
    ('Block 20', 'Block 20'),
    ('Block 21', 'Block 21'),
    ('Block 23', 'Block 23'),
    ('Block 26', 'Block 26'),
    ('Block 27', 'Block 27'),
    ('Block 28', 'Block 28'),
    ('Block 29', 'Block 29'),
    ('Block 30', 'Block 30'),
    ('Block 32', 'Block 32'), 
    ('Block 33', 'Block 33'),
    ('Block 34', 'Block 34'),
    ('Block 35', 'Block 35'),
    ('Block 37', 'Block 37'),
    ('Block 38', 'Block 38'),
    ('Block 39', 'Block 39'), 
    ('Argos Block', 'Argos Block'),
    ('Main Cafeteria', 'Main Cafeteria'),
    ('Cafeteria 2', 'Cafeteria 2'),
    ('North Parking Lot', 'North Parking Lot'),
    ('South Parking Lot', 'South Parking Lot'),
    ('Guayabos Parking Lot', 'Guayabos Parking Lot'),
    ('Synthetic fields - Main Cafeteria', 'Synthetic fields - Main Cafeteria'),
    ('Synthetic fields - North Parking Lot', 'Synthetic fields - North Parking Lot') ]

CATEGORY_CHOICES = [
    ('Technology', 'Technology'),
    ('Keys', 'Keys'),
    ('Books', 'Books'),
    ('Water Bottles', 'Water Bottles'),
    ('Headphones', 'Headphones'),
    ('Lunchboxes', 'Lunchboxes'),
    ('Clothes', 'Clothes'),
    ('Accessories', 'Accessories'),
    # ... continue adding categories
]






def delete_object(request, object_id):
    objects_complaints = Object.objects.filter(complaints_amount__gt=2)

    data = get_user_data(request)
    if data is not None:
        user_role = data['profile_role']
    else:
        user_role = 'guest'
    obj_to_delete = get_object_or_404(Object, pk=object_id)
    if request.method == "GET":
        print("gettt")
        obj_to_delete.delete()
    return render(request, 'app\my_objects.html', {'user_role': user_role, 'objects_complaints': objects_complaints})


















#Funcion para mandar los correos con los links de verificacion de la cuenta. 
def send_email(email_user,verification_link):
    load_dotenv()
    email_sender ="seek.ueafit@gmail.com"
    password = os.getenv("PASSWORD")
    email_reciver = email_user
    subject = "VERIFICATION ACCOUNT SEEK-U"
    body= "Hello\n"+"You registered an account on [Seek-U], before being able to\nuse your account you need to verify that this is your email address by clicking here: ["+verification_link+"]" 
    
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_reciver
    em["Subject"] = subject
    em.set_content(body)
    
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL("smtp.gmail.com",465,context = context) as smtp:
        smtp.login(email_sender,password)
        smtp.sendmail(email_sender,email_reciver,em.as_string())
        
#Function that add to the collection a user
def create_Collectio_User(email,mobile_phone,profile_role,user_uid,password,name):
    coleccion_ref = db.collection('usuario_eafit')
    nuevo_documento = {
        'user_id':user_uid, 
        'email':email, 
        'name' : name,
        'mobile_phone': mobile_phone,
        'profile_role': profile_role,
        'password': password
    }   
    coleccion_ref.document(user_uid).set(nuevo_documento)
class ClaimObjectView(View):
    objects_complaints = Object.objects.filter(complaints_amount__gt=2)

    def get(self,request):
        objects_complaints = Object.objects.filter(complaints_amount__gt=2)

        data = get_user_data(request)
        if data is not None:
            user_role = data['profile_role']
        else:
            user_role = 'guest'
        form=ClaimObject()
        return render(request,"app/claim_req.html",{'form':form, 'user_role':user_role, 'objects_complaints': objects_complaints})
    def post(self,request):
        pass
class ClaimObjectView_es(View):
    def get(self,request):
        objects_complaints = Object.objects.filter(complaints_amount__gt=2)

        data = get_user_data(request)
        if data is not None:
            user_role = data['profile_role']
        else:
            user_role = 'guest'
        form=ClaimObject_es()
        return render(request,"app/claim_req_es.html",{'form':form, 'user_role':user_role, 'objects_complaints': objects_complaints})
    def post(self,request):
        pass 
    
@login_required  
def filterObjects(request):
    data = get_user_data(request)
    if data is not None:
        user_role = data['profile_role']
    else:
        user_role = 'guest'
    place=request.POST.get('place_found','')
    date=request.POST.get('date_found','datetime')
    color = request.POST.get('color', '')
    brand = request.POST.get('brands', '')
    request.session["place_found"]=place
    request.session['color']=color
    request.session['brand']=brand
    filtered_objects = Object.objects.filter(color=color, brands=brand,place_found=place,date_found__gte=date)
    print(filtered_objects)
    return render(request,"app/index2.html",{'objects': filtered_objects, 'user_role':user_role, 'objects_complaints': objects_complaints})

@login_required  
def filterObjects_es(request):
    data = get_user_data(request)
    if data is not None:
        user_role = data['profile_role']
    else:
        user_role = 'guest'
    place=request.POST.get('place_found','')
    date=request.POST.get('date_found','datetime')
    color = request.POST.get('color', '')
    brand = request.POST.get('brands', '')
    request.session["place_found"]=place
    request.session['color']=color
    request.session['brand']=brand
    filtered_objects = Object.objects.filter(color=color, brands=brand,place_found=place,date_found__gte=date)
    print(filtered_objects)
    return render(request,"app/index2_es.html",{'objects': filtered_objects, 'user_role':user_role, 'objects_complaints': objects_complaints})


@login_required
def count_objects(request):
    data = get_user_data(request)
    if data is not None:
        user_role = data['profile_role']
    else:
        user_role = 'guest'
    # Retrieve the counts of objects for each block from the database
    block_counts = Object.objects.values('place_found').annotate(count=Count('place_found'))
    
    # Pass the block-wise object counts as a context variable to the template
    context = {
        'block_counts': block_counts, 'user_role':user_role, 'objects_complaints': objects_complaints
    }
    
    return render(request, 'app/index2.html', context)


@login_required
def count_objects_es(request):
    data = get_user_data(request)
    if data is not None:
        user_role = data['profile_role']
    else:
        user_role = 'guest'
    # Retrieve the counts of objects for each block from the database
    block_counts = Object.objects.values('place_found').annotate(count=Count('place_found'))
    
    # Pass the block-wise object counts as a context variable to the template
    context = {
        'block_counts': block_counts, 'user_role':user_role
    }
    
    return render(request, 'app/index2_es.html', context)

def send_email2(email_user,description,subject_):
    load_dotenv()
    email_sender ="seek.ueafit@gmail.com"
    password = os.getenv("PASSWORD")
    email_reciver = email_user
    subject = subject_
    body= description
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_reciver
    em["Subject"] = subject
    em.set_content(body,subtype="html")
    
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL("smtp.gmail.com",465,context = context) as smtp:
        smtp.login(email_sender,password)
        smtp.sendmail(email_sender,email_reciver,em.as_string())

@login_required
def NotifyMe(request):
    place=request.session.get('place_found')
    color=request.session.get('color')
    brand=request.session.get('brand')
    email=request.user.email
    Noti.objects.create(brands=brand,color=color,place_found=place,user_email=email)
    print("hola",place,color,brand)
    return redirect(reverse("home"))

@login_required
def claiming(request,id):
    try:
        object_to_edit = get_object_or_404(Object, pk=id)
        print(id)
        object_to_edit.object_status="Claimed"
        subject="Object claimed"
        description=f"""
        <p>Your claimed object has an ID {id}</p>
        """
        send_email2(request.user.email,description,subject)
        object_to_edit.save()
    except:
        pass
    return redirect(reverse("home"))