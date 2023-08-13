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

#Librerias para mandar correos automaticos
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
# Create your views here.

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
            # Redirigir a la página de inicio de sesión u otra página deseada
            return redirect(reverse('login')) 

        except Exception as e:
            error_message = str(e)
            if hasattr(e, 'error_info') and hasattr(e.error_info, 'message'):
                error_message = str(e.error_info.message)
            print('Error al registrar usuario:', error_message)
            return render(request, 'app/register.html', {'error_message': error_message})

    return render(request, 'app/register.html') 


def login(request):
     if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = auth.get_user_by_email(email)
            if user.email_verified:
                auth_pyrebase.sign_in_with_email_and_password(email, password)
                # Generar el token personalizado
                custom_token = auth.create_custom_token(str(user.uid))
                return render(request, 'dashboard.html', {'custom_token': custom_token})  # Puedes pasar el token a tu template si lo necesitas
        except:
            print("oli")
        return render(request, "app/login.html")

def home(request):
    return render(request, "app/home.html")







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
