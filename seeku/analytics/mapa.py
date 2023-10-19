from .models import Object
import folium # drawing library
import webbrowser
import os # auxiliary library to save the map
from folium.plugins import MarkerCluster # jmarkers
from streamlit_folium import st_folium
import streamlit as st
from django.db.models import Count
from .models import Object



m = folium.Map(location=[6.20020215, -75.5784848084993], # generates map 
            zoom_start=35)


blocks_coords = {'Block 1': (6.201924560701277, -75.57630045012571), 'Block 3': (6.199872207434223, -75.57858824729921), 'Block  4': (6.19966635220012, -75.57840693003529), 'Block 7': (6.1992557075961185, -75.57811725146168), 'Block 9': (6.197358205212653, -75.57960104968517), 'Block 10': (6.197432868160243, -75.5799121859309), 'Block 12': (6.197299541460698, -75.57905387904613), 'Block 13': (6.19831815659064, -75.57885539557903), 'Block 14': (6.198536811938063, -75.57888221766918), 'Block 15': (6.198672271554982, -75.57886183261873), 'Block 16': (6.198896259808183, -75.5788564682007), 'Block 17': (6.199082916613181, -75.57891547679901), 'Block 18': (6.199381567363811, -75.57892084121706), 'Block 19': (6.197978973978083, -75.57969868183137), 'Block 20': (6.1984802815479965, -75.57923197746278), 'Block 21': (6.198442950149637, -75.57954847812654), 'Block 23': ( 6.1989, -75.5793), 'Block 26': (6.199845542220294, -75.57910966879719), 'Block 27': (6.200362847129584, -75.57915258414143), 'Block 28': (6.200362847129584, -75.57893800742023), 'Block 29': (6.200400178392071, -75.5786805153548), 'Block 30': (6.200613499922653, -75.57907640933992), 'Block 32': (6.2010753406174555, -75.57843053344186), 'Block 33': (6.200910016646622, -75.57900452617106), 'Block 34': (6.201096672738934, -75.57901525500712), 'Block 35': (6.201288661793546, -75.57900452617106), 'Block 37': (6.20204595125134, -75.57884359379386), 'Block 38': (6.201667306648228, -75.57841980476952), 'Block 39': (6.2019552898922585, -75.5783983470974), 'Argos Block': (6.199261040604284, -75.5793060063661), 'Main Cafeteria': (6.199197044014476, -75.57851743691572), 'Cafeteria 2': (6.201546780370403, -75.5789862870188), 'North Parking Lot': (6.201653440751808, -75.57772457599641), 'South Parking Lot': (6.197660056689131, -75.57870519171048), 'Guayabos Parking Lot': (6.2015670458026175, -75.57627618345579), 'Synthetic fields - Main Cafeteria': (6.198583742846361, -75.57857000798323), 'Synthetic fields - North Parking Lot': (6.202338200678335, -75.5783275362228)}

objetos_por_lugar = Objeto.objects.values('place_found').annotate(total=Count('place_found'))

cantidades = []

for lugar_info in objetos_por_lugar:
    lugar = lugar_info['place_found']
    cantidad_objetos = lugar_info['total']
    cantidades.append(cantidad_objetos)

index = 0
for name, coords in blocks_coords.items():
    cantidad = cantidades[index]
    marker = folium.Marker(
        location=[coords[0], coords[1]],
        popup=name,  # Puedes personalizar esto según tu número o etiqueta
        icon=folium.DivIcon(
        )
    ).add_to(m)
    index = index+1

m.save(os.path.join('Path.html'))
webbrowser.open_new_tab('Path.html')