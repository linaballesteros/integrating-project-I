#Librerias para manejar firebase, son firebase_admin y pyrebase
from django.shortcuts import render
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
            create_Collectio_User(user.email,user.phone_number,'regular',user.uid,password)
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
            if True:
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
                    return redirect('claim_request')  # Cambia 'admin_dashboard' por la URL de la página del admin
                elif user_role == 'regular':
                    return redirect('home')  # Cambia 'home' por la URL de la página del usuario regular
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

# Decorador para verificar roles
def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Obtener el uid del usuario autenticado en Firebase (de tu proceso de login)
            user_uid = request.session.get('user_uid')  # Asegúrate de almacenar el uid en la sesión

            # Consultar Firestore para obtener el rol del usuario
            user_doc = db.collection('usuario_eafit1').document(user_uid).get()
            user_role = user_doc.get('profile_role')

            # Verificar si el rol del usuario está en los roles permitidos
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('home')  # Redirigir al inicio si no tiene permisos

        return _wrapped_view
    return decorator

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
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

@login_required
def claim_request(request):
    return render(request, "app\claim_request.html")

def my_profile(request):
    return render(request, "app\profile.html")

def history(request):
    return render(request, "app\history.html")

def publish_object(request):
    return render(request, "app\publish_object.html")

def my_objects(request):
    objects = Object.objects.all()  # Retrieve all objects from the database
    return render(request, 'my_objects.html', {'objects': objects})

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
            return redirect('app\index2.html')  # Redirect 
        else:
            print(form.errors)  # Print form errors to the console for debugging
    else:
        form = ObjectForm()

    return render(request, 'app\index2.html', {'form': form})

def delete_object(request, object_id):
  obj_to_delete = get_object_or_404(Object, pk=object_id)
  if request.method == "GET":
      print("gettt")
      obj_to_delete.delete()
  return render(request, 'app\edit_object.html')


















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
def create_Collectio_User(email,mobile_phone,profile_role,user_uid,password):
    coleccion_ref = db.collection('usuario_eafit')
    nuevo_documento = {
        'user_id':user_uid, 
        'email':email, 
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