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
        # ofertas=soup.find("div", attrs={"class":"itemProduct n1colunas"}).findAll("ul", attrs={"class":""}) 
        ofertas=soup.find("div", attrs={"id":"gallery-layout-container"}).findAll("li")
    except:
        ofertas=[]
        print("no se encontro ninguna oferta")
    if len(ofertas) != 0 :
        for oferta in ofertas:
            ofertaAdd=[]
            oferta_info = {}

            try:
                oferta_info["imagen"] = oferta.find("img")['src']
            except:
                oferta_info["imagen"] = "NO ESPECIFICADO"

            ofertaAdd.append(oferta_info["imagen"])
                
            try:
                oferta_info["nombre"] = oferta.find("span", attrs={"class":"vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body"}).get_text()

            except:
                oferta_info["nombre"] = "NO ESPECIFICADO"
            
            ofertaAdd.append(oferta_info["nombre"])

            try:
                oferta_info["tipoMoneda"] = oferta.find("span", attrs={"class":"vtex-product-price-1-x-currencyCode vtex-product-price-1-x-currencyCode--summary"}).get_text()

            except:
                oferta_info["tipoMoneda"] = "NO ESPECIFICADO"

            ofertaAdd.append(oferta_info["tipoMoneda"])


            try:
                
                precioActualEntero=oferta.find("span", attrs={"class":"vtex-product-price-1-x-currencyInteger vtex-product-price-1-x-currencyInteger--summary"}).get_text()
                precioActualDecimal=oferta.find("span", attrs={"class":"vtex-product-price-1-x-currencyFraction vtex-product-price-1-x-currencyFraction--summary"}).get_text()
                
                oferta_info["precioActual"] = precioActualEntero + "." + precioActualDecimal

            except:
                oferta_info["precioActual"] = "NO ESPECIFICADO"


            ofertaAdd.append(oferta_info["precioActual"])

        
            try:

                precioAnteriorEntero=oferta.find("span", attrs={"class":"vtex-product-price-1-x-listPrice"}).find("span", attrs={"class":"vtex-product-price-1-x-currencyInteger"}).get_text()
                precioAnteriorDecimal=oferta.find("span", attrs={"class":"vtex-product-price-1-x-listPrice"}).find("span", attrs={"class":"vtex-product-price-1-x-currencyFraction"}).get_text()
                
                oferta_info["precioAnterior"] = precioAnteriorEntero + "." + precioAnteriorDecimal

            except:
                oferta_info["precioAnterior"] = oferta_info["precioActual"]

            ofertaAdd.append(oferta_info["precioAnterior"])


            try:
                oferta_info["descuento"] = oferta.find("span", attrs={"class":"vtex-product-price-1-x-savingsPercentage"}).get_text()

            except:
                oferta_info["descuento"] = "NO TIENE DESCUENTO"


            ofertaAdd.append(oferta_info["descuento"])


            lista_ofertas.append(ofertaAdd)
        
        lista_ofertas.insert(0, ["Imagen", "Nombre", "Tipo de Moneda", "Precio Actual", "Precio Anterior", "Descuento"])

    
    return lista_ofertas

