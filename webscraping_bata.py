# -*- coding: utf-8 -*-
from urllib.request import urlopen
from urllib.error import HTTPError
import bs4
from bs4 import BeautifulSoup
import requests


def scraping_ofertas(url_busqueda):
    lista_ofertas = []       
    url = url_busqueda

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
 
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    try:
        ofertas=soup.find("div", attrs={"class":"itemProduct n1colunas"}).findAll("ul", attrs={"class":""}) 
    except:
        ofertas=[]
        print("no se encontro ninguna oferta")
    if len(ofertas) != 0 :
        for oferta in ofertas:
            oferta_info = {}
            try:
                oferta_info["imagen"] = oferta.find("img")['src']
                print(oferta_info["imagen"])
            except:
                oferta_info["imagen"] = "NO ESECIFICADO"
                print("no se encontro el imagen")
                
            try:
                oferta_info["marca"] = oferta.find("h3", attrs={"class":"productbrand"}).get_text()
                print(oferta_info["marca"])

            except:
                oferta_info["marca"] = "NO ESECIFICADO"
                print("no se encontro el marca")
            
            try:
                oferta_info["nombre"] = oferta.find("h2", attrs={"class":"productNames"}).get_text()
                print(oferta_info["nombre"])

            except:
                oferta_info["nombre"] = "NO ESECIFICADO"
                print("no se encontro el nombre")
                
            try:
                oferta_info["precio"] = oferta.find("p", attrs={"class":"precio bestPrice"}).find("span", attrs={"class":"normal"}).get_text()
                print(oferta_info["precio"])

            except:
                oferta_info["precio"] = oferta.find("p", attrs={"class":"precio ex-precio"}).find("span", attrs={"class":"ahora"}).get_text()
                print(oferta_info["precio"])
            lista_ofertas.append(oferta_info)
            print("---------------------")
            # print(oferta_info)
    
    return lista_ofertas

