from django.shortcuts import render
import folium # map library
import webbrowser
from folium.plugins import MarkerCluster # markers
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
# Connect with the utils and app
from app.models import Object
from utils.choises import CATEGORY_CHOICES, HOUR_CHOICES, COLOR_CHOICES, BLOCK_CHOICES, OFFICE_CHOICES, STATUS_CHOICES, RECOVERED_CHOICES
from utils.forms import ObjectForm, ClaimObject
from accounts.views import login_required

# Create your views here.



@login_required
def analytics(request):
    
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


    return render(request, 'app\_analytics.html', {'labels': labels, 'counts': counts, 'months': months, 'counts2': counts2, 'places': places, 'counts3': counts3, 'hours': hours, 'counts4': counts4},)

@login_required
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

def path(request):
    return render(request, "app\Path.html")