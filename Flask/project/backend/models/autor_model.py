from project.backend.models.postgres_connection_pool import PostgreSQLPool  

class AutorModel:
    def __init__(self):        
        self.postgres_pool = PostgreSQLPool() 

    def get_autor(self, autor_id):    
        params = {'autor_id' : autor_id}      
        rv = self.postgres_pool.execute("SELECT * from autores where autor_id=%(autor_id)s", params)                
        data = []
        content = {}
        for result in rv:
            content = {
                'autor_id': result[0], 
                'nombre': result[1], 
                'apellido': result[2], 
                'nacionalidad': result[3], 
                'fecha_nacimiento': result[4]
            }
            data.append(content)
            content = {}
        return data

    def get_autores(self):  
        rv = self.postgres_pool.execute("SELECT * from autores")  
        data = []
        content = {}
        for result in rv:
            content = {
                'autor_id': result[0], 
                'nombre': result[1], 
                'apellido': result[2], 
                'nacionalidad': result[3], 
                'fecha_nacimiento': result[4]
            }
            data.append(content)
            content = {}
        return data

    def create_autor(self, nombre, apellido, nacionalidad, fecha_nacimiento):    
        data = {
            'nombre' : nombre,
            'apellido' : apellido,
            'nacionalidad': nacionalidad,
            'fecha_nacimiento': fecha_nacimiento
        }  
        query = """insert into autores (nombre, apellido, nacionalidad, fecha_nacimiento) 
            values (%(nombre)s, %(apellido)s, %(nacionalidad)s, %(fecha_nacimiento)s)"""    
        cursor = self.postgres_pool.execute(query, data, commit=True)   

        data['autor_id'] = cursor.lastrowid 
        return data

    def update_autor(self, autor_id, nombre, apellido, nacionalidad, fecha_nacimiento):    
        data = {
            'autor_id' : autor_id,
            'nombre' : nombre,
            'apellido' : apellido,
            'nacionalidad': nacionalidad,
            'fecha_nacimiento': fecha_nacimiento
        }  
        query = """update autores set nombre = %(nombre)s, apellido = %(apellido)s,
                    nacionalidad = %(nacionalidad)s, fecha_nacimiento = %(fecha_nacimiento)s 
                    where autor_id = %(autor_id)s"""    
        cursor = self.postgres_pool.execute(query, data, commit=True)   

        result = {'result': 1}  # Confirma que la actualización fue exitosa
        return result

    def delete_autor(self, autor_id):    
        params = {'autor_id' : autor_id}      
        query = """delete from autores where autor_id = %(autor_id)s"""    
        self.postgres_pool.execute(query, params, commit=True)   

        result = {'result': 1}  # Confirma que la eliminación fue exitosa
        return result
