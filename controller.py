
from dboperation import DBWebscraping
from dboperation import DBOferta
from dboperation import DBOfertadetalle
from dboperation import DBkeyWord
#JOSEF
from dboperation import DBKeyworSearch

class Controller:
    def __init__(self):
        self.dbwebscraping = DBWebscraping()
        self.dboferta = DBOferta()
        self.dbofertadetalle = DBOfertadetalle()
        self.dbkeyword = DBkeyWord()
        #JOSEF
        self.dbkeywordsearch = DBKeyworSearch()


    def registrar_restaurante(self, con, restaurante):
        id = self.dbwebscraping.insert_restaurante(con, restaurante)
        return id

    def registrar_detalle_restaurante(self, con, restaurante):        
        self.dboferta.insert_detalle(con, restaurante)

    ##metodo añadido para insertar las tuplas del detalle de la oferta
    def registrar_detalle_oferta(self, con, listaDetalle):
        #print(listaDetalle)
        idOfertaDetalle=self.dbofertadetalle.insertOfertaDetalle(con, listaDetalle)            
        

    def registrar_comida(self, con, lista_comida):
        self.dboferta.insert_comida(con, lista_comida)     

    def generar_insert_ofertadetalle(self, oferta):
        sql_insert = "INSERT INTO OFERTA_DETALLE (id_oferta,descripcion,fecha_creacion,fecha_modificacion) VALUES (%s,'%s',sysdate,sysdate);"
        sql_result = ""
        for ed in oferta["listaDescripcion"]:
            sql = sql_insert % (oferta["idPuesto"], ed)
            sql_result = sql_result + sql
        return sql_result


    #prepara descripcion en una lista de diccionarios para el insert en oferta_detalle
    def analizaSegundoLi(self,tuplas, row):
        tuplafinal=[]
        avisotupla=str(tuplas).replace("<li>","").replace("</li>","").split("<br/>")
        for aviso in avisotupla:
            a={}
            if aviso.strip():
                a["id_oferta"]= row
                a["descripcion"]=aviso.strip()
                tuplafinal.append(a)
        return tuplafinal


    def getwords(self, conn):
        return self.dbkeyword.getwords(conn)

    def evitar_redundancia(self, con, oferta):
        return self.dboferta.evitar_redundancia(con, oferta)


    #JOSEFF
    def registrar_oferta_detalle(self, con, oferta_detalle):
        idResult = self.dbofertadetalle.insertOfertaDetalleJOSEFF(con, oferta_detalle)    

    def obtener_keyword_search(self, con):  
        return self.dbkeywordsearch.obtener_descripcion(con)