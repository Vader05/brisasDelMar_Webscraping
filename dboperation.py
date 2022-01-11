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
        mydb = connection.connect()
        try:
            #mydb = connection.connect()
            cur = mydb.cursor()                                    
            sql = "insert into restaurante_detalle (id_restaurante, rango_precio, horario_atencion, pagina_web, direccion) values (%s,%s,%s,%s,%s)"            
            params = (detalle["id_restaurante"], detalle["precio"].strip(), detalle["horario"].strip(), detalle["web"].strip(),detalle["direccion"].strip())
            cur.execute(sql, params)        
            mydb.commit()            
            
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
        mydb = connection.connect()
        try:
            #mydb = connection.connect()
            cur = mydb.cursor()                                    
            sql = "insert into comida_restaurante (nombre, id_restaurante) values (%s,%s)"            
            params = (oferta["nombre"], oferta["id_restaurante"])
            cur.execute(sql, params)        
            mydb.commit()            
            
            # close the communication with the PostgreSQL
            cur.close()
            mydb.close()                           

        except (Exception, psycopg2.DatabaseError) as error:                
            print ("-------------Exception, psycopg2.DatabaseError-------------------")
            print (error)
            mydb.close()        
            



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
                mydb.close()        
            
        return array_de_tuplas
