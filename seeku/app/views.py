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
from firebase_admin import credentials, auth, firestore, initialize_app
import pyrebase
from django.shortcuts import redirect
from django.contrib import messages
from firebase_admin._auth_utils import handle_auth_backend_error
from django.urls import reverse
from .models import Object
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
from .forms import ObjectForm, ClaimObject
from datetime import datetime

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


initialize_app(cred)
db = firestore.client()


firebase = pyrebase.initialize_app(config)
auth_pyrebase = firebase.auth()
#--------------------------------------------------------------------------------------------------------

#Start de functions for the page. 

#Function that help to register and verificate ther user in the database
def register_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['mobile_phone']
        country_phone = request.POST['country_code']
        name = request.POST['name']
        phone_complete = country_phone+phone

        try:
            #Verifica que el dominio sea de @eafit.edu.co
            if not email.endswith('@eafit.edu.co'):
                error_message = "Por favor, use un correo electrónico válido de @eafit.edu.co"
                return render(request, 'app/register.html', {'error_message': error_message})
            
            if len(password) < 6:
                error_message = "La contrasena no es lo suficientemente larga"
                return render(request, 'app/register.html', {'error_message': error_message})
            
            user = auth.create_user(email=email, password=password, phone_number=phone_complete)
            # Crear usuario en Firebase Auth
            print("Usuario creado:", user.email)
            # Generar enlace de verificación y enviar correo
            link = auth.generate_email_verification_link(email)
            print("Correo de verificación enviado")
            print("Enlace de verificación:", link)
            send_email(user.email,link)
            #Add to the collection the user with the role, "regular"
            create_Collectio_User(user.email,user.phone_number,'regular',user.uid,password,name)
            # Redirigir a la página de inicio de sesión u otra página deseada
            return redirect(reverse('login')+'?email_verification=true') 

        except Exception as e:
            error_message = str(e)
            if hasattr(e, 'error_info') and hasattr(e.error_info, 'message'):
                error_message = str(e.error_info.message)
            print('Error al registrar usuario:', error_message)
            return render(request, 'app/register.html', {'error_message': error_message})

    return render(request, 'app/register.html') 
 


#Function that help to connect the user with the database, and depend of the user_role have some actions. 
def login(request):
    
    #Show in the screen a message to the user for verificate de email. 
     email_verification = request.GET.get('email_verification')
     if email_verification == 'true':
        message = "Por favor, verifica tu correo electrónico antes de iniciar sesión."
     else:
        message = ""

     if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = auth.get_user_by_email(email)
            if user.email_verified:
                auth_pyrebase.sign_in_with_email_and_password(email, password)
                # Generar el token personalizado
                # Obtener el uid del usuario autenticado (esto puede variar según cómo almacenes el uid en tu sesión)
                user_uid = user.uid
                # Almacenar el uid en la sesión para usarlo posteriormente
                request.session['user_uid'] = user_uid
                # Consultar Firestore para obtener el rol del usuario
                user_doc = db.collection('usuario_eafit').document(user_uid).get()
                user_role = user_doc.get('profile_role')
                if user_role == 'admin':
                    print("entro aqui")
                    return redirect('publish_object')  # Cambia 'admin_dashboard' por la URL de la página del admin
                elif user_role == 'regular':
                    return redirect('search')  # Cambia 'home' por la URL de la página del usuario regular
            else:
                error_message = "Por favor, verifica tu correo electronico"
                return render(request, 'app/login.html', {'error_message': error_message})
        except Exception as e:
            error_message = str(e)
            if hasattr(e, 'error_info') and hasattr(e.error_info, 'message'):
                error_message = str(e.error_info.message)
            print('Error al inicar sesion:', error_message)
            #error_message = "Credenciales inválidas. Por favor, verifica tus datos."
            return render(request, 'app/login.html', {'error_message': error_message})
        
     return render(request, 'app/login.html', {'message': message})

def is_user_authenticated(request):
    try:
        # Verifica si existe un token de autenticación en la sesión del usuario
        user_uid = request.session.get('user_uid')
        if user_uid:
            return True
        else:
            return False
    except Exception as e:
        # Manejar la excepción específica aquí, por ejemplo, imprimir un mensaje de registro
        print(f"Error al verificar la autenticación del usuario: {str(e)}")
        return False


def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_user_authenticated(request):
            print(request.session.get('user_uid'))
            return redirect('login')  # Redirige a la página de inicio de sesión si el usuario no ha iniciado sesión
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def home(request):
    searchTerm = request.GET.get('searchObject')
    if searchTerm:
        objects = Object.objects.filter(title__icontains=searchTerm)        
    elif searchTerm == False:
        objects = Object.objects.all()
    else:
        return render(request, "app\index.html")        
    return render(request, "app\index2.html", {'searchTerm': searchTerm, 'objects': objects})   

# @login_required
def search(request):
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

    return render(request, "app\index2.html", {'searchTerm': searchTerm, 'objects': objects})

    
    """
    searchTerm = request.GET.get('searchObject')
    category = request.GET.get('category') 
    # place_found = request.GET.get('place')
    
    objects = Object.objects.all()
    # Filter objects based on search term and category
    if searchTerm:
        objects = Object.objects.filter(title__icontains=searchTerm)   
    elif searchTerm == False:
        objects = Object.objects.all()
    else:
        return render(request, "app\index2.html")     
    # Apply category filter 
    if category:
        objects = objects.filter(category=category)
    """
    """
    
    if place_found == "Blocks 1-10":
        objects = objects.filter(category=place_found[0])
        
    elif place_found == "Blocks 11-15":
        objects = objects.filter(category=place_found[1])
        
    elif place_found == "Blocks 16-21":
        objects = objects.filter(category=place_found[2])
    
    elif place_found == "Blocks 22-30":
        objects = objects.filter(category=place_found[3])
        
    elif place_found == "Blocks 31-38":
        objects = objects.filter(category=place_found[4])
        
    else:
        objects = objects.filter(category=place_found)
    """
    return render(request, "app/index2.html", {'searchTerm': searchTerm, 'objects': objects, 'category': category})

def claim_request(request):
    return render(request, "app\claim_request.html")

def my_profile(request):
    return render(request, "app\profile.html")

def edit_profile_view(request):
     return render(request, "app\edit_profile.html")
 
def history(request):
    print("entró a history")
    # Consulta la base de datos para obtener los objetos con object_status igual a "Claimed" para mostrarlos en el historial
    objetos_claimed = Object.objects.filter(object_status="Claimed")
    print(objetos_claimed)
    return render(request, 'app\history.html', {'objetos_claimed': objetos_claimed})
 
def analytics(request):
    
    print("entro a analytics")
    
    # por categorias
    data = Object.objects.values('category').annotate(count=Count('category'))
    

    labels = [item['category'] for item in data]
    counts = [item['count'] for item in data]

    print("Labels:", labels)
    print("Counts:", counts)

    # meses 
    data2 = Object.objects.annotate(month=TruncMonth('date_found'))
    data2 = data2.values('month').annotate(count=Count('id'))

    months = [item['month'].strftime('%B') for item in data2]
    counts2 = [item['count'] for item in data2]
    
    print("Months:", months)
    print("Counts2:", counts2)
    
    # Obtener los 10 lugares con la mayor cantidad de objetos perdidos
    data_places = Object.objects.values('place_found').annotate(count=Count('id')).order_by('-count')[:10]

    places = [item['place_found'] for item in data_places]
    counts3 = [item['count'] for item in data_places]

    print("Places:", places)
    print("Counts Places:", counts3)
    
    # horarios 
    data_hours = Object.objects.values('hour_range').annotate(count=Count('id'))

    hours = [item['hour_range'] for item in data_hours]
    counts4 = [item['count'] for item in data_hours]

    print("Hours:", hours)
    print("Counts Hours:", counts4)
    
    # claim y not claimed
    
    data_status = Object.objects.values('object_status').annotate(count=Count('id'))

    status = [item['object_status'] for item in data_status]
    counts5 = [item['count'] for item in data_status]

    print("Object Status:", status)
    print("Counts Status:", counts5)
    
    
    return render(request, 'app\_analytics.html', {'labels': labels, 'counts': counts, 'months': months, 'counts2': counts2, 'places': places, 'counts3': counts3, 'hours': hours, 'counts4': counts4, 'status': status, 'counts5': counts5})

def map_view(request):
   # para mostrar el mapa:
    
    m = folium.Map(location=[6.20020215, -75.5784848084993], # generates map 
            zoom_start=35)


    blocks_coords = {'Block 1': (6.201924560701277, -75.57630045012571), 'Block 3': (6.199872207434223, -75.57858824729921), 'Block  4': (6.19966635220012, -75.57840693003529), 'Block 7': (6.1992557075961185, -75.57811725146168), 'Block 9': (6.197358205212653, -75.57960104968517), 'Block 10': (6.197432868160243, -75.5799121859309), 'Block 12': (6.197299541460698, -75.57905387904613), 'Block 13': (6.19831815659064, -75.57885539557903), 'Block 14': (6.198536811938063, -75.57888221766918), 'Block 15': (6.198672271554982, -75.57886183261873), 'Block 16': (6.198896259808183, -75.5788564682007), 'Block 17': (6.199082916613181, -75.57891547679901), 'Block 18': (6.199381567363811, -75.57892084121706), 'Block 19': (6.197978973978083, -75.57969868183137), 'Block 20': (6.1984802815479965, -75.57923197746278), 'Block 21': (6.198442950149637, -75.57954847812654), 'Block 23': ( 6.1989, -75.5793), 'Block 26': (6.199845542220294, -75.57910966879719), 'Block 27': (6.200362847129584, -75.57915258414143), 'Block 28': (6.200362847129584, -75.57893800742023), 'Block 29': (6.200400178392071, -75.5786805153548), 'Block 30': (6.200613499922653, -75.57907640933992), 'Block 32': (6.2010753406174555, -75.57843053344186), 'Block 33': (6.200910016646622, -75.57900452617106), 'Block 34': (6.201096672738934, -75.57901525500712), 'Block 35': (6.201288661793546, -75.57900452617106), 'Block 37': (6.20204595125134, -75.57884359379386), 'Block 38': (6.201667306648228, -75.57841980476952), 'Block 39': (6.2019552898922585, -75.5783983470974), 'Argos Block': (6.199261040604284, -75.5793060063661), 'Main Cafeteria': (6.199197044014476, -75.57851743691572), 'Cafeteria 2': (6.201546780370403, -75.5789862870188), 'North Parking Lot': (6.201653440751808, -75.57772457599641), 'South Parking Lot': (6.197660056689131, -75.57870519171048), 'Guayabos Parking Lot': (6.2015670458026175, -75.57627618345579), 'Synthetic fields - Main Cafeteria': (6.198583742846361, -75.57857000798323), 'Synthetic fields - North Parking Lot': (6.202338200678335, -75.5783275362228)}
    
    lugares_con_cantidad = Object.objects.values('place_found').annotate(cantidad_objetos=Count('id'))
    
    places2 = [item['place_found'] for item in lugares_con_cantidad]
    counting = [item['cantidad_objetos'] for item in lugares_con_cantidad]
    
    # Usar una comprensión de diccionario para combinar las dos listas en un diccionario
    places_and_counts = {places2[i]: counting[i] for i in range(len(places2))}
    print("a ver diccccionario")
    print(places_and_counts)
    
    print(places2)
    print(counting)
    
    for name, coords in blocks_coords.items():
    # Obtener la cantidad de objetos para este lugar
        cantidad_objetos = places_and_counts.get(name, 0)

        # Personalizar el icono HTML con la cantidad de objetos
        icon_html = f'<div style="background-color: blue; color: white; border: 2px solid #2E64FE; border-radius: 50%; width: 24px; height: 24px; text-align: center; font-size: 14px; line-height: 24px;">{cantidad_objetos}</div>'

        # Agregar el marker al mapa
        folium.Marker(
            location=[coords[0], coords[1]],
            popup=name,
            icon=folium.DivIcon(html=icon_html)
        ).add_to(m)
    
    m.save(os.path.join('Path.html'))
    
    webbrowser.open_new_tab('Path.html')
    
    return render(request, 'app\_analytics.html')


def publish_object(request):
    return render(request, "app\publish_object.html")



def  my_objects(request):
    objects = Object.objects.all()  # Retrieve all objects from the database
    return render(request, 'my_objects.html', {'objects': objects})

def about(request):
    return render(request, "app\_about.html")


def path(request):
    return render(request, "app\Path.html")

# analytics






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
         return render(request, 'my_objects.html', {'object_to_edit' : object_to_edit})   
    else:
        form = ObjectForm()
        return render(request, 'edit_object.html', {'object_to_edit' : object_to_edit})

  

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
    obj_to_delete = get_object_or_404(Object, pk=object_id)
    if request.method == "GET":
        print("gettt")
        obj_to_delete.delete()
    return render(request, 'app\my_objects.html')


















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
    
def filterObjects(request):
    place=request.GET.get('place_found','')
    date=request.GET.get('date_found','datetime')
    color = request.GET.get('color', '')
    brand = request.GET.get('brands', '')
    filtered_objects = Object.objects.filter(color=color, brands=brand,place_found=place,date_found__gte=date)
    print(filtered_objects)
    return render(request,"app/index2.html",{'objects': filtered_objects})

def count_objects(request):
    # Retrieve the counts of objects for each block from the database
    block_counts = objects.values('place_found').annotate(count=Count('place_found'))
    
    # Pass the block-wise object counts as a context variable to the template
    context = {
        'block_counts': block_counts,
    }
    
    return render(request, 'app/index2.html', context)