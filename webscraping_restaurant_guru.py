# -*- coding: utf-8 -*-
from urllib.request import urlopen
from urllib.error import HTTPError
import bs4
from bs4 import BeautifulSoup
import requests
from controller import Controller
from configuration import RESTAURANT_GURU
import unicodedata

from datetime import date
from datetime import datetime
from datetime import timedelta

def contain_br(contents):
    for element in contents:
        if type(element) is bs4.element.Tag:
            if element.name == "br":
                return True
    return False


def get_content(contents):
    lista = []
    for element in contents:
        if type(element) is bs4.element.NavigableString:
            if str(element) is not None and str(element).strip() != "":
                lista.append(str(element))
    return lista


def scraping_ofertas(url_principal, url_busqueda, id_carga):
    controller = Controller()
    lista_oferta = []       
    
    url = url_busqueda

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
 
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    try:
        restaurantes=soup.findAll("div", attrs={"class":"restaurant_row show"})  
    except:
        restaurantes=[]
        print("no se encontro nada")

    if len(restaurantes) != 0 :
        for rest in restaurantes:
            rest_info = {}
            rest_url = rest.find("a")['href']
            page = requests.get( rest_url, headers= headers)
            restaurantInfoPage = BeautifulSoup(page.text ,"lxml")

            try:
                rest_info["nombre"] = restaurantInfoPage.find("h1", attrs={"class":"notranslate"}).get_text()
            except:
                rest_info["nombre"] = "NO ESECIFICADO"
                print("no se encontro el nombre")
                
            try:
                rest_info["precio"] = restaurantInfoPage.find("div", attrs={"class":"short_info with_avg_price"}).get_text()
            except:
                rest_info["precio"] = "NO ESECIFICADO"
                print("no se encontro el precio")
            
            try:
                rest_info["horario"] = restaurantInfoPage.findAll("td", attrs={"class":"current-day"})[1].get_text()
            except:
                rest_info["horario"] = "NO ESECIFICADO"
                print("no se encontro el horario")
                
            try:
                comidas = restaurantInfoPage.findAll("div", attrs={"class":"groupdiv"})[3]
                print(comidas)
                rest_info["platos"] = comidas.findChildren()
            except:
               
                rest_info["platos"] = "NO ESECIFICADO"
                print("no se encontro los platos")
            lista_oferta.append(rest_info)
            print(rest_info)
    
    return lista_oferta


def scraping_ofertadetalle(url_pagina, row_id, con):
    controller = Controller()
    detalle = {}
    detalle["id_oferta"] = row_id
    print(detalle["id_oferta"])
    req = requests.get(url_pagina)
    soup = BeautifulSoup(req.text, "lxml")
    
    contenido = soup.find("div", attrs={"class": "col-md-12 descripcion-texto"})
    try: 
        str_list = elimina_tildes(contenido.decode_contents().replace("</p>", '').replace("<p>", '').replace("-", '').replace("•", '').strip()).split('<BR/>')
    except: 
        str_list = []
        
    str_list = list(filter(None, str_list))

    #print(str_list)
    """
    try:
        contenido_extra = soup.findAll("div", attrs={"class": "row oferta-contenido"})
        str_list2 = elimina_tildes(contenido_extra[-1].get_text().replace("•", '')).splitlines()
        str_list2 = list(filter(None, str_list2))
    except:
        str_list2 = []
    """
    #print(str_list2)



    for s_contenido in str_list:
        detalle["descripcion"] = s_contenido.strip()[0:2000]
        controller.registrar_oferta_detalle(con, detalle)
    
    """
    for s_contenido_x in str_list2:
        detalle["descripcion"] = s_contenido_x.strip()
        controller.registrar_oferta_detalle(con, detalle)
    """
    return 1


def replace_quote(list):
    new_list = []
    for el in list:
        el = el.replace("'", "''")
        new_list.append(el)
    return new_list


def obtener_lista_keywords(con):
    controller = Controller()
    lista_busquedas = []
    for search in controller.obtener_keyword_search(con): 
        busqueda = {}
        if search != None:
            busqueda["id"] = search[0]
            busqueda["descripcion"] = search[1].replace(" ", "-")
            lista_busquedas.append(busqueda)

    return lista_busquedas


def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
    return s.upper()

def fecha_publicacion(modalidad, tiempo):
    #[-1] = mes-dias-ayer-hoy
    #[-2]= 25-publicado-un
    tiemponum = 1
    if(tiempo == "UN"):
        tiemponum = 1

    tiempo = int(tiemponum)
    switcher = {
        "HORAS": datetime.now() + timedelta(days=-tiempo/24),       
        "DIA":   datetime.now() + timedelta(days=-1),
        "DIAS":  datetime.now() + timedelta(days=-tiempo),
        "MES":   datetime.now() + timedelta(days=-30),
        "MESES": datetime.now() + timedelta(days=-tiempo*30)
    }
    return switcher.get(modalidad,datetime.now())