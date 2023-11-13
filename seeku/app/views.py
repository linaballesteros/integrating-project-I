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
from .models import Object, Noti,Claim_Complaint,Search,HistorySearches
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
from .forms import ObjectForm, ClaimObject, ClaimComplaint
from datetime import datetime
from accounts.views import login_required
from profile_user.views import get_user_data
from django.core.mail import send_mail
#Connect to firebase data. 
#-------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

#Start de functions for the page. 


@login_required
def search(request):
    data = get_user_data(request)
    user_role = data['profile_role']
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

    return render(request, "app\index2.html", {'searchTerm': searchTerm, 'objects': objects, 'user_role': user_role})

   
   
@login_required
def claim_request(request):
    data = get_user_data(request)
    user_role = data['profile_role']
    return render(request, "app\claim_request.html", {'user_role': user_role})

@login_required
def history(request):
    data = get_user_data(request)
    user_role = data['profile_role']
    print("entró a history")
    # Consulta la base de datos para obtener los objetos con object_status igual a "Claimed" para mostrarlos en el historial
    objetos_claimed = Object.objects.filter(object_status="Claimed")
    print(objetos_claimed)
    return render(request, 'app\history.html', {'objetos_claimed': objetos_claimed, 'user_role': user_role})


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
    data = get_user_data(request)
    user_role = data['profile_role']
    obj_to_delete = get_object_or_404(Object, pk=object_id)
    if request.method == "GET":
        print("gettt")
        obj_to_delete.delete()
    return render(request, 'app\my_objects.html', {'user_role': user_role})


















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
    def get(self,request):
        form=ClaimObject()
        return render(request,"app/claim_req.html",{'form':form})
    def post(self,request):
        pass
@login_required
def filterObjects(request):
    place=request.POST.get('place_found','')
    date=request.POST.get('date_found','datetime')
    color = request.POST.get('color', '')
    brand = request.POST.get('brands', '')
    description=request.POST.get('user_comment','')
    request.session["place_found"]=place
    request.session['color']=color
    request.session['brand']=brand
    request.session['date']=date
    request.session['description']=description
    email=request.user.email
    try:
        searched=Search.objects.get(place_found=place, date_found=date, color=color, brands=brand)
    except:
        searched=Search.objects.create(place_found=place, date_found=date, color=color, brands=brand)
    try:
        history_search=HistorySearches.objects.get(object_related=searched,user_email=email)
        history_search.quantity+=1
        history_search.save()
    except:
        history_search=HistorySearches.objects.create(object_related=searched,user_email=email,quantity=1)
    seven_days_ago = datetime.now().date() - timedelta(days=7)
    if len(list(HistorySearches.objects.filter(user_email=email,date_searched__gte=seven_days_ago)))>2:
        print("Suspicious behavior")
    filtered_objects = Object.objects.filter(color=color, brands=brand,place_found=place,date_found__gte=date)
    not_allowed_objects=filtered_objects.filter(user_claimer=email).values_list('id',flat=True)
    not_allowed_objects2=Claim_Complaint.objects.filter(user_email=email).values_list('object_related',flat=True)
    print(list(not_allowed_objects))
    return render(request,"app/index2.html",{'objects': filtered_objects,'unallowed':list(not_allowed_objects),'unallowed2':list(not_allowed_objects2)})

@login_required
def count_objects(request):
    # Retrieve the counts of objects for each block from the database
    block_counts = Object.objects.values('place_found').annotate(count=Count('place_found'))
    
    # Pass the block-wise object counts as a context variable to the template
    context = {
        'block_counts': block_counts,
    }
    
    return render(request, 'app/index2.html', context)
def send_email2(email_user,description,subject_,parametro=True):
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
    if parametro:
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
        object_to_edit.user_claimer=request.user.email
        subject="Object claimed"
        description=f"""
        <p>Your claimed object has an ID {id}</p>
        """
        send_email2(request.user.email,description,subject)
        object_to_edit.save()
    except:
        pass
    return redirect(reverse("home"))
@login_required
def claim_complaint(request,id,method=2):
    lost_object=get_object_or_404(Object,id=id)
    if request.method=="POST":
        form=ClaimComplaint(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            Claim_Complaint.objects.create(time_initial=cd['time_initial'],
                                          time_final=cd['time_final'],
                                          date_lost=request.session['date'],
                                          extra_data=request.session['description']+'\n'+cd['extra_data'],
                                          object_related=lost_object,
                                          user_email=request.user.email,
                                          
                                          )
            print("object created")
            if method==2:
                return redirect(reverse("home"))
            else:
                return redirect(reverse('claiming',args=(id,)))
    else:
        form=ClaimComplaint()
        return render(request, 'app/claim_complaint.html',{'form':form})
def claim_complaints_views(request):
    emails=Object.objects.exclude(user_claimer__isnull=True).values_list('user_claimer',flat=True).distinct()
    #list_ids=Claim_Complaint.objects.exclude(object_related__user_claimer=F('user_email')).values_list('object_related',flat=True)
    #objects=Object.objects.filter(id__in=list_ids).distinct()
    objects=Object.objects.filter(complaints_amount__gte=2).distinct()
    return render(request, 'app/complaints.html',{'objects':objects})
def claim_complaint_detail_view(request,id):
    objects=Claim_Complaint.objects.filter(object_related=id)
    if objects:
        return render(request, 'app/complaint_claimers.html',{'objects':objects, 'length':len(list(objects))})
    else:
        return redirect(reverse('claim_complaints_view'))
def claim_complaint_script(request, id, user_email,parametro):
    object=Claim_Complaint.objects.get(object_related=id,user_email=user_email)
    object.delete()
    thing=Object.objects.get(id=id)
    description=f"""
    Color: {thing.color}\n
    Brand: {thing.brands}\n
    Place found: {thing.place_found}"""
    if parametro:
        description="Your claim request was rejected because the entered data was false\n"+ description
    else:
        description=f"Your claim request was accepted, you can claim your object with the id {thing.id}\n"+description
    send_email2(user_email,description,"Claim complaint",False)
    return redirect(reverse('claim_complaint_detail', args=(id,)))

