import psycopg2


class DBWebscraping:
    def __init__(self):
        pass

    def insert_restaurante(self, connection, carga):
        mydb = connection.connect()
        try:
          #mydb = connection.connect()         
          cur = mydb.cursor() 
          # insertando un registro
          sql = "insert into restaurante (nombre, especialidad, id_region) VALUES(%s,%s,%s)"
          params = (carga["nombre"], carga["especialidad"], carga["id_region"])
          cur.execute(sql, params)                 
          mydb.commit()

          sql = "SELECT last_value FROM restaurante_id_seq"
          cur.execute(sql)  
          id_restaurante = int(cur.fetchone()[0])
          
          # close the communication with the PostgreSQL
          cur.close()
          mydb.close()      
        except (Exception, psycopg2.DatabaseError) as error:                
            print (error)
            mydb.close()
        return id_restaurante
    

class DBOferta:
    def __init__(self):
        pass

    def insert_detalle(self, connection, detalle):        
        # id_restaurante_detalle=0
        mydb = connection.connect()
        try:
            #mydb = connection.connect()
            cur = mydb.cursor()                                    
            sql = "insert into restaurante_detalle (id_restaurante, rango_precio, horario_atencion, pagina_web, direccion) values (%s,%s,%s,%s,%s)"            
            params = (detalle["id_restaurante"], detalle["precio"].strip(), detalle["horario"].strip(), detalle["web"].strip(),detalle["direccion"].strip())
            cur.execute(sql, params)        
            mydb.commit()            

            # sql = "SELECT last_value FROM restaurante_detalle_id_seq"
            # cur.execute(sql)  
            # id_restaurante_detalle = int(cur.fetchone()[0])
            #print(id_oferta)  
            
            # close the communication with the PostgreSQL
            cur.close()
            mydb.close()                           

        except (Exception, psycopg2.DatabaseError) as error:                
            print ("-------------Exception, psycopg2.DatabaseError-------------------")
            print (error)
            print("insertar oferta ERROR")
            mydb.close()        
            
        # return id_restaurante_detalle
    
    def insert_comida(self, connection, oferta):        
        # id_comida=0
        mydb = connection.connect()
        try:
            #mydb = connection.connect()
            cur = mydb.cursor()                                    
            sql = "insert into comida_restaurante (nombre, id_restaurante) values (%s,%s)"            
            params = (oferta["nombre"], oferta["id_restaurante"])
            cur.execute(sql, params)        
            mydb.commit()            

            # sql = "SELECT last_value FROM comida_restaurante_id_comida_seq"
            # cur.execute(sql)  
            # id_comida = int(cur.fetchone()[0])
            #print(id_oferta)  
            
            # close the communication with the PostgreSQL
            cur.close()
            mydb.close()                           

        except (Exception, psycopg2.DatabaseError) as error:                
            print ("-------------Exception, psycopg2.DatabaseError-------------------")
            print (error)
            print("insertar oferta ERROR")
            mydb.close()        
            
        # return id_comida

class DBOfertadetalle:
    def __init__(self):
        pass

    def update_ofertadetalle(self, connection, requisito):
        mydb = connection.connect()
        try:
            mycursor = mydb.cursor()
            sql = "UPDATE OFERTA_DETALLE SET descripcion_normalizada=:1 where id_ofertadetalle=:2"
            params = (requisito["descripcion_normalizada"], requisito["iddescripcion"])

            mycursor.execute(sql, params)
            mydb.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print ("-------------Exception, psycopg2.DatabaseError-------------------")
            print (error)
            print("OFERTA DETALLE UPDATE OFERTA_DETALLE ERROR")
            mydb.close()

    def insertOfertaDetalle(self, connection, listaDetalle):
        mydb = connection.connect()
        try:
            #mydb= connection.connect()
            mycursor= mydb.cursor()

            for detalle in listaDetalle:
                sql= "insert into oferta_detalle ( id_ofertadetalle, id_oferta, descripcion, fecha_creacion, fecha_modificacion) values (DEFAULT,%s,%s,current_date,current_date)"
                params= (detalle["id_oferta"],detalle["descripcion"].strip())
                mycursor.execute(sql, params)
                mydb.commit()

            # close the communication with the PostgreSQL
            mycursor.close()
            mydb.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print ("-------------Exception, psycopg2.DatabaseError-------------------")
            print (error)
            print("OFERTA DETALLE INSERTAR OFERTA_DETALLE ERROR")
            mydb.close()
        
        return 1
    def insertOfertaDetalleJOSEFF(self, connection, detalle):
        try:
            mydb= connection.connect()
            mycursor= mydb.cursor()
            sql= "insert into oferta_detalle ( id_ofertadetalle, id_oferta, descripcion, fecha_creacion, fecha_modificacion) values (DEFAULT,%s,%s,current_date,current_date)"
            params= (detalle["id_oferta"],detalle["descripcion"])
            mycursor.execute(sql, params)
            mydb.commit()
            # close the communication with the PostgreSQL
            mycursor.close()
            mydb.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print ("-------------Exception, psycopg2.DatabaseError-------------------")
            print (error)
            mydb.close()
            
        return 1
        
class DBkeyWord:
    def __init__(self):
        pass

    def getwords(self,connection):
        mydb= connection.connect()
        try:
            #mydb= connection.connect()
            mycursor= mydb.cursor()
            sql= "select id_keyword, descripcion from keyword_search"
            mycursor.execute(sql)
            palabras= list(mycursor)
            
            # close the communication with the PostgreSQL
            mycursor.close()
            mydb.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print ("-------------Exception, psycopg2.DatabaseError-------------------")
            print (error)
            print("KEYWORD ERROR")
            mydb.close()
        
        return palabras

#JOSEF
class DBKeyworSearch:
    def __init__(self):
        pass

    def obtener_descripcion(self, connection):        
        try:
            mydb = connection.connect()
            cur = mydb.cursor()                                    

            sql = "SELECT id_region, capital_departamento FROM region_restaurante"
            cur.execute(sql)  
            
            array_de_tuplas = []
            row = cur.fetchone()
            while row is not None:
                array_de_tuplas.append(row)
                row = cur.fetchone()

            # close the communication with the PostgreSQL
            cur.close()
            mydb.close()                           

        except (Exception, psycopg2.DatabaseError) as error:                
                print ("-------------Exception, psycopg2.DatabaseError-------------------")
                print (error)
                print("JOSEFF ERROR")
                mydb.close()        
            
        return array_de_tuplas

class DatesDB:
    def __init__(self):
        pass

    

#RESETEAR FECHAS
#update oferta set fecha_publicacion=null;