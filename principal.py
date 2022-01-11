# -*- coding: utf-8 -*-
from configuration import *
from controller import Controller
from dbconnection import Connection
from dboperation import DatesDB
import webscraping_restaurant_guru

# metodo para la conxión a la DB
def connect_bd():
    con = Connection(
        DATABASE["DB_HOST"],
        DATABASE["DB_SERVICE"],
        DATABASE["DB_USER"],
        DATABASE["DB_PASSWORD"],
    )
    con.connect()
    return con


def brisasDelMar():
    controller = Controller()
    con = connect_bd()
    carga = {}
    carga["pagina"] = RESTAURANT_GURU["WS_PORTAL_LABORAL"]
    carga["url_principal"] = RESTAURANT_GURU["WS_PORTAL_LABORAL_URL"]

    for type_search in webscraping_restaurant_guru.obtener_lista_keywords(con):
        print(type_search)
        carga["url_busqueda"] = carga["url_principal"] + type_search["descripcion"]
        carga["id_keyword"] = type_search["id"]
        # carga["id_carga"] = controller.registrar_webscraping(con, carga)

        listaOferta = webscraping_restaurant_guru.scraping_ofertas(
            con, carga["url_busqueda"],carga["id_keyword"]
        )
    


def test():
    lista = webscraping_restaurant_guru.scraping_ofertas(
            RESTAURANT_GURU["WS_PORTAL_LABORAL_URL"], RESTAURANT_GURU["WS_PORTAL_LABORAL_URL"]+"Lima", 1
        )
    
    # print('desde test',lista)
    
    
if __name__ == "__main__":
    brisasDelMar()
    # test()
