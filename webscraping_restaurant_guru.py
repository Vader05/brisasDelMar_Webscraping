# -*- coding: utf-8 -*-
from urllib.request import urlopen
from urllib.error import HTTPError
import bs4
from bs4 import BeautifulSoup
import requests
from controller import Controller
from configuration import RESTAURANT_GURU



def scraping_ofertas(con, url_busqueda, id_region):
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
            rest_info["id_region"]=id_region
            rest_url = rest.find("a")['href']
            page = requests.get( rest_url, headers= headers)
            restaurantInfoPage = BeautifulSoup(page.text ,"lxml")

            try:
                rest_info["nombre"] = restaurantInfoPage.find("h1", attrs={"class":"notranslate"}).get_text().replace('\n',"")
            except:
                rest_info["nombre"] = "NO ESPECIFICADO"
                print("no se encontro el nombre")
                
            try:
                rest_info["precio"] = restaurantInfoPage.find("div", attrs={"class":"short_info with_avg_price"}).get_text().replace('\n',"").replace('$',"")[36:].replace('-',"")
            except:
                rest_info["precio"] = "NO ESPECIFICADO"
                print("no se encontro el precio")
            
            try:
                rest_info["horario"] = restaurantInfoPage.findAll("td", attrs={"class":"current-day"})[1].get_text()
            except:
                rest_info["horario"] = "NO ESPECIFICADO"
                print("no se encontro el horario")
                

            try:
                rest_info["direccion"] = restaurantInfoPage.find("div", attrs={"class":"address"}).findAll("div")[1].get_text().replace('\n',"")
            except:
                rest_info["direccion"] = "NO ESPECIFICADO"
                print("no se encontro la direccion")
                
            
            
            try:
                rest_info["especialidad"] = restaurantInfoPage.find("div", attrs={"class":"cuisine_wrapper"}).get_text().replace('\n',"")
            except:
                rest_info["especialidad"] = "NO ESPECIFICADO"
                print("no se encontro la especialidad")

            try:
                rest_info["web"] = restaurantInfoPage.find("div", attrs={"class":"website"}).findAll("div")[1].find("a").get_text().replace('\n',"")
                print(rest_info["web"])
            except:
                rest_info["web"] = "NO ESPECIFICADO"
                print("no se encontro la web")
                
        
            try:
                comidas=""
                comidas1 = restaurantInfoPage.find("div", attrs={"class":"f_meals"}).findAll("span")
                for comida in comidas1:
                    comidas=comidas.replace('\n',"")+comida.get_text().replace('\n',"")+'-'
                rest_info["platos"] = comidas
            except:
                rest_info["platos"] = "NO ESPECIFICADO"
                print("no se encontro los platos")

            lista_oferta.append(rest_info)
            print(rest_info)

            rest_info["id_restaurante"]=controller.registrar_restaurante(con, rest_info)
            controller.registrar_detalle_restaurante(con, rest_info)
            controller.registrar_comida(con, rest_info)

    return lista_oferta


def obtener_lista_keywords(con):
    controller = Controller()
    lista_busquedas = []
    for search in controller.obtener_keyword_search(con): 
        busqueda = {}
        if search != None:
            busqueda["id"] = search[0]
            busqueda["descripcion"] = search[1]
            lista_busquedas.append(busqueda)

    return lista_busquedas


