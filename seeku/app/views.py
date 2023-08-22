#Librerias para manejar firebase, son firebase_admin y pyrebase
from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render
from django.views.generic import View
from firebase_admin import credentials, auth, firestore, initialize_app
import pyrebase
from django.shortcuts import redirect
from django.contrib import messages
from firebase_admin._auth_utils import handle_auth_backend_error
from django.urls import reverse
from .models import Object
from django.http import HttpResponse
from functools import wraps
#Librerias para mandar correos automaticos
from dotenv import load_dotenv 
import os
from email.message import EmailMessage
import ssl
import smtplib

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
        return render(request, "app/index.html")        
    return render(request, "app\index2.html", {'searchTerm': searchTerm, 'objects': objects})   


def search(request):
    searchTerm = request.GET.get('searchObject')
    if searchTerm:
        objects = Object.objects.filter(title__icontains=searchTerm)        
    else:
        objects = Object.objects.all()
    return render(request, "app\index2.html", {'searchTerm': searchTerm, 'objects': objects})

@login_required
def claim_request(request):
    return render(request, "app\index3.html")





















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
