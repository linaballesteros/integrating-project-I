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
#Send emails :)
from dotenv import load_dotenv 
import os
from email.message import EmailMessage
import ssl
import smtplib
from datetime import datetime

from django.contrib.auth import login


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
#--------------------------------------------------------------------------------------------------------



#Function that help to register and verificate ther user in the database
def register_es(request):
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
                return render(request, 'register.html', {'error_message': error_message})
            
            if len(password) < 6:
                error_message = "La contrasena no es lo suficientemente larga, minimo de 6"
                return render(request, 'register.html', {'error_message': error_message})
            
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
            return render(request, 'register_es.html', {'error_message': error_message})

    return render(request, 'register_es.html') 
 
def register(request):
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
                error_message = "Plase use a valid email with @eafit.edu.co"
                return render(request, 'register.html', {'error_message': error_message})
            
            if len(password) < 6:
                error_message = "Passwords must contain at least 6 characters"
                return render(request, 'register.html', {'error_message': error_message})
            
            user = auth.create_user(email=email, password=password, phone_number=phone_complete)
            # Crear usuario en Firebase Auth
            print("Created user:", user.email)
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
            return render(request, 'register.html', {'error_message': error_message})

    return render(request, 'register.html') 

#Function that help to connect the user with the database, and depend of the user_role have some actions. 
def login(request):
    
    #Show in the screen a message to the user for verificate de email. 
     email_verification = request.GET.get('email_verification')
     if email_verification == 'true':
        message = "Please verify your email before logging in."
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
                request.session['email']=email
                # Consultar Firestore para obtener el rol del usuario
                user_doc = db.collection('usuario_eafit').document(user_uid).get()
                user_role = user_doc.get('profile_role')
                if user_role == 'admin':
                    request.session['user_uid'] = user_uid  # Almacena el UID del usuario en la sesión de Django
                    print("entro aqui")
                    return redirect('publish_object')
                elif user_role == 'regular':
                    request.session['user_uid'] = user_uid  # Almacena el UID del usuario en la sesión de Django
                    return redirect('search')  # Redirigir a la página del usuario regular

            else:
                error_message = "Please, verify your email"
                return render(request, 'login.html', {'error_message': error_message})
        except Exception as e:
            error_message = str(e)
            if hasattr(e, 'error_info') and hasattr(e.error_info, 'message'):
                error_message = str(e.error_info.message)
            print('Error Trying to Log In,', error_message)
            #error_message = "Credenciales inválidas. Por favor, verifica tus datos."
            return render(request, 'login.html', {'error_message': error_message})
        
     return render(request, 'login.html', {'message': message})
 
def login_es(request):
    
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
                    request.session['user_uid'] = user_uid  # Almacena el UID del usuario en la sesión de Django
                    print("entro aqui")
                    return redirect('publish_object')
                elif user_role == 'regular':
                    request.session['user_uid'] = user_uid  # Almacena el UID del usuario en la sesión de Django
                    return redirect('search')  # Redirigir a la página del usuario regular

            else:
                error_message = "Por favor verifica tu correo electrónico"
                return render(request, 'login_es.html', {'error_message': error_message})
        except Exception as e:
            error_message = str(e)
            if hasattr(e, 'error_info') and hasattr(e.error_info, 'message'):
                error_message = str(e.error_info.message)
            print('Error Trying to Log In,', error_message)
            #error_message = "Credenciales inválidas. Por favor, verifica tus datos."
            return render(request, 'login_es.html', {'error_message': error_message})
        
     return render(request, 'login_es.html', {'message': message})
 
 
#Function to send email
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
    object_user = {}
    nuevo_documento = {
        'user_id':user_uid, 
        'email':email, 
        'name' : name,
        'mobile_phone': mobile_phone,
        'profile_role': profile_role,
        'password': password,
        'objects': object_user, 
    }   
    coleccion_ref.document(user_uid).set(nuevo_documento)
    
def login_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        # Verificar si el user_uid está presente en la sesión
        if 'user_uid' in request.session:
            # El usuario ha iniciado sesión correctamente, puedes acceder a user_uid
            user_uid = request.session['user_uid']
            # Lógica adicional si es necesario
            return f(request, *args, **kwargs)
        else:
            # El usuario no ha iniciado sesión, redirigir a la página de inicio de sesión
            login_url = reverse('login')  # Obtiene la URL de inicio de sesión basada en el nombre
            return redirect(login_url)  # Redirige al usuario a la página de inicio de sesión
    return decorated_function


