# -*- coding: utf-8 -*-
import webscraping_bata
import csv



def caso_estudio_bata():
    pagina_url="https://www.bata.pe/ofertas"
    bataOfertas=webscraping_bata.scraping_ofertas(pagina_url)
    
    return bataOfertas
    
    
if __name__ == "__main__":
    # caso_estudio_bata()
    with open("dataOfertasBata.csv","w", newline='') as file:
        writter=csv.writer(file,delimiter=";")
        writter.writerows(caso_estudio_bata())
