
from dboperation import DBWebscraping
from dboperation import DBOferta
from dboperation import DBKeyworSearch

class Controller:
    def __init__(self):
        self.dbwebscraping = DBWebscraping()
        self.dboferta = DBOferta()
        self.dbkeywordsearch = DBKeyworSearch()


    def registrar_restaurante(self, con, restaurante):
        id = self.dbwebscraping.insert_restaurante(con, restaurante)
        return id

    def registrar_detalle_restaurante(self, con, restaurante):        
        self.dboferta.insert_detalle(con, restaurante)

    def registrar_comida(self, con, lista_comida):
        self.dboferta.insert_comida(con, lista_comida)     

    def obtener_keyword_search(self, con):  
        return self.dbkeywordsearch.obtener_descripcion(con)