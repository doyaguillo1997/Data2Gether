
######################################################Funciones y paquetes necesarios:
import json
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from math import floor, ceil
import numpy as np
import pickle as pk
from datetime import date

#Funcion para guardar archivos .pickle:
def save_data(datt, name):
    with open(name, 'wb') as file:
        pk.dump(datt, file, protocol = pk.HIGHEST_PROTOCOL)
   
#Funcion para leer archivos .pickle:   
def open_data(name):
    with open(name,'rb') as file:
        globals()[name] = pk.load(file)
    
#Funcion para solicitar permiso para usar la api:    
def get_oauth_token(key, secret):
    oauth_url = "https://api.idealista.com/oauth/token"
    payload = {"grant_type": "client_credentials"}
    r = requests.post(oauth_url, auth=HTTPBasicAuth(key, secret), data=payload)
    return r.text

#Funcion para hacer consulta a la api:
def search_api(url, token):
    api_url = url
    headers = {"Authorization": "Bearer " + token}
    r = requests.post(api_url, headers = headers)
    return r.text

#Funcion para crear la url de la consulta, en base a los parametros
#de centro, radio, precio maximo y precio minimo:
def crear_url(center, distance, maxPrice, minPrice):
     return ('https://api.idealista.com/3.5/es/search?operation=sale' + 
           '&maxItems=50' +
           '&center='+ center +
           '&distance='+ distance +
           '&propertyType=homes' +
           '&numPage=%s' +
           '&language=es' + 
           '&minPrice=' + minPrice +
           '&maxPrice=' + maxPrice)
    

#Funcion para hacer una sola peticion a la api:
def peticion_unica(clave, contrasena, centro_coordenadas, 
                   radio_coordenadas, precio_minimo, precio_maximo):
    
    token_json = get_oauth_token(clave, contrasena)
    token_response = json.loads(token_json)
    token_value = token_response["access_token"]
    search_json = search_api(crear_url(center = centro_coordenadas, distance = radio_coordenadas,
                                       maxPrice = precio_maximo, 
                                       minPrice = precio_minimo), token_value)
    search_response = json.loads(search_json)
    datos_consulta = pd.DataFrame.from_dict(search_response['elementList'])
    datos_consulta['FechaConsulta'] = date.today().strftime("%Y/%m/%d")
    return datos_consulta
  
    
#Funcion para realizar todas las peticiones posibles:        
def peticion_multiple(datos_key, barrio, num_consultas, centro_coordenadas, 
                      radio_coordenadas, precio_minimo, precio_maximo):
    
    num_key = 1
    
    #Calculo los intervalos de precios iniciales:
    amplitud_intervalos = (precio_maximo - precio_minimo)/num_consultas
    intervalos = []
    for consulta in range(num_consultas):
        minimo = precio_minimo + amplitud_intervalos*consulta
        maximo = precio_minimo + amplitud_intervalos*(consulta + 1)
        intervalos.append((floor(minimo), floor(maximo)))
        

    #Hago las peticiones con los intervalos iniciales:
    peticiones_por_revisar = []
    for consulta in range(num_consultas):
        try:
            globals()[barrio + str(consulta + 1)] = peticion_unica(datos_key['Key'][num_key], 
                   datos_key['Password'][num_key], centro_coordenadas, radio_coordenadas, 
                   str(intervalos[consulta][0]), str(intervalos[consulta][1]))
        except:
            num_key = num_key + 1
            globals()[barrio + str(consulta + 1)] = peticion_unica(datos_key['Key'][num_key], 
                   datos_key['Password'][num_key], centro_coordenadas, radio_coordenadas, 
                   str(intervalos[consulta][0]), str(intervalos[consulta][1]))
        save_data(globals()[barrio + str(consulta + 1)], barrio + str(consulta + 1))
        peticiones_por_revisar.append((barrio + str(consulta + 1),
                                       intervalos[consulta][0],
                                       intervalos[consulta][1]))
        
    #Hago las peticiones con profundidad 1:
    peticiones_por_revisar2 = []
    for peticion in peticiones_por_revisar:
        if len(globals()[peticion[0]]) == 50:
            intervalos = [peticion[1], 
                          floor(np.mean([peticion[1], peticion[2]])),
                          peticion[2]]
            
            #Primera peticion:
            try:
                globals()[peticion[0] + '_1'] = peticion_unica(datos_key['Key'][num_key], 
                       datos_key['Password'][num_key], centro_coordenadas, radio_coordenadas, 
                       str(intervalos[0]), str(intervalos[1]))
            except:
                num_key = num_key + 1
                globals()[peticion[0] + '_1'] = peticion_unica(datos_key['Key'][num_key], 
                       datos_key['Password'][num_key], centro_coordenadas, radio_coordenadas, 
                       str(intervalos[0]), str(intervalos[1]))
            save_data(globals()[peticion[0] + '_1'], peticion[0] + '_1')
            peticiones_por_revisar2.append((peticion[0] + '_1', intervalos[0], intervalos[1]))
            
            #Segunda peticion:
            try:
                globals()[peticion[0] + '_2'] = peticion_unica(datos_key['Key'][num_key], 
                       datos_key['Password'][num_key], centro_coordenadas, radio_coordenadas, 
                       str(intervalos[1]), str(intervalos[2]))
            except:
                num_key = num_key + 1
                globals()[peticion[0] + '_2'] = peticion_unica(datos_key['Key'][num_key], 
                       datos_key['Password'][num_key], centro_coordenadas, radio_coordenadas, 
                       str(intervalos[1]), str(intervalos[2]))
            save_data(globals()[peticion[0] + '_2'], peticion[0] + '_2')
            peticiones_por_revisar2.append((peticion[0] + '_2', intervalos[1], intervalos[2]))
            
    
    #Hago las peticiones con profundidad 2:
    for peticion in peticiones_por_revisar2:
        if len(globals()[peticion[0]]) == 50:
            intervalos = [peticion[1], 
                          floor(np.mean([peticion[1], peticion[2]])),
                          peticion[2]]
            
            #Primera peticion:
            try:
                globals()[peticion[0] + '_1'] = peticion_unica(datos_key['Key'][num_key], 
                       datos_key['Password'][num_key], centro_coordenadas, radio_coordenadas,
                       str(intervalos[0]), str(intervalos[1]))
            except:
                num_key = num_key + 1
                globals()[peticion[0] + '_1'] = peticion_unica(datos_key['Key'][num_key], 
                       datos_key['Password'][num_key], centro_coordenadas, radio_coordenadas,
                       str(intervalos[0]), str(intervalos[1]))
            save_data(globals()[peticion[0] + '_1'], peticion[0] + '_1')
            
            #Segunda peticion:
            try:
                globals()[peticion[0] + '_2'] = peticion_unica(datos_key['Key'][num_key], 
                       datos_key['Password'][num_key],centro_coordenadas, radio_coordenadas, 
                       str(intervalos[1]), str(intervalos[2]))
            except:
                num_key = num_key + 1
                globals()[peticion[0] + '_2'] = peticion_unica(datos_key['Key'][num_key], 
                       datos_key['Password'][num_key],centro_coordenadas, radio_coordenadas, 
                       str(intervalos[1]), str(intervalos[2]))
            save_data(globals()[peticion[0] + '_2'], peticion[0] + '_2')
            
            
            
            
######################################################Realizacion de las peticiones:
            
#Excel donde se tienen todas las keys del grupo:
datos_key = pd.read_excel('../concesiones keys.xlsx')

#Excel donde se tiene toda la informacion necesaria de los barrios, para poder
#hacer las consultas con los parametros deseados:
datos_barrio = pd.read_excel('../datos barrios.xlsx')[['BARRIO', 'N CONSULTAS (ABARQUE TOTAL)', 
                            'PRECIO MIN', 'PRECIO MAX', 'COORDENADAS', 'RADIO']]

#Se realizan las peticiones para cada barrio:
for barrio_selec in list(datos_barrio['BARRIO']):
    seleccion = datos_barrio[datos_barrio['BARRIO'] == barrio_selec]
    barrio = seleccion['BARRIO'].str.cat()
    num_consultas = int(seleccion['N CONSULTAS (ABARQUE TOTAL)'])
    centro_coordenadas = (seleccion['COORDENADAS'].str.cat().split('\xa0')[1] + ',' + 
                          seleccion['COORDENADAS'].str.cat().split('\xa0')[0])
    radio_coordenadas = str(ceil(float(seleccion['RADIO'])*6.366/60*1000000))
    precio_minimo = int(seleccion['PRECIO MIN'])
    precio_maximo = int(seleccion['PRECIO MAX'])
    peticion_multiple(datos_key, barrio, num_consultas, centro_coordenadas, 
                      radio_coordenadas, precio_minimo, precio_maximo)
    
    
    
    