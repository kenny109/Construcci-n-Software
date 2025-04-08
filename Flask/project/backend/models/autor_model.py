from project.backend.models.postgres_connection_pool import PostgreSQLPool

class AutorModel:
    def __init__(self):
        self.postgres_pool = PostgreSQLPool()

    def get_autor(self, autor_id):
        params = {'autor_id': autor_id}
        rv = self.postgres_pool.execute("""
            SELECT * FROM autores WHERE autor_id=%(autor_id)s AND activo=TRUE
        """, params)
        
        data = []
        for result in rv:
            content = {
                'autor_id': result[0],
                'nombre': result[1],
                'apellido': result[2],
                'nacionalidad': result[3],
                'fecha_nacimiento': result[4].strftime('%Y-%m-%d') if result[4] else None
            }
            data.append(content)
        
        return data

    def get_autores(self):
        rv = self.postgres_pool.execute("SELECT * FROM autores WHERE activo=TRUE")
        
        data = []
        for result in rv:
            content = {
                'autor_id': result[0],
                'nombre': result[1],
                'apellido': result[2],
                'nacionalidad': result[3],
                'fecha_nacimiento': result[4].strftime('%Y-%m-%d') if result[4] else None
            }
            data.append(content)
        
        return data

    def get_libros_by_autor(self, autor_id):
        params = {'autor_id': autor_id}
        rv = self.postgres_pool.execute("""
            SELECT l.libro_id, l.titulo, l.anio_publicacion
            FROM libros l
            INNER JOIN libro_autor la ON l.libro_id = la.libro_id
            WHERE la.autor_id = %(autor_id)s AND l.activo = TRUE
        """, params)
        
        data = []
        for result in rv:
            content = {
                'libro_id': result[0],
                'titulo': result[1],
                'anio_publicacion': result[2]
            }
            data.append(content)
        
        return data

    def create_autor(self, nombre, apellido, nacionalidad, fecha_nacimiento):
        data = {
            'nombre': nombre,
            'apellido': apellido,
            'nacionalidad': nacionalidad,
            'fecha_nacimiento': fecha_nacimiento
        }
        
        query = """INSERT INTO autores (nombre, apellido, nacionalidad, fecha_nacimiento)
                VALUES (%(nombre)s, %(apellido)s, %(nacionalidad)s, %(fecha_nacimiento)s)
                RETURNING autor_id"""
                
        autor_id = self.postgres_pool.execute(query, data, commit=True)
        
        data['autor_id'] = autor_id
        return data

    def update_autor(self, autor_id, nombre, apellido, nacionalidad, fecha_nacimiento):
        # Verificar si el autor existe
        params = {'autor_id': autor_id}
        rv = self.postgres_pool.execute("SELECT autor_id FROM autores WHERE autor_id=%(autor_id)s AND activo=TRUE", params)
        
        if not rv:
            return {'error': 'Autor no encontrado o inactivo'}
        
        data = {
            'autor_id': autor_id,
            'nombre': nombre,
            'apellido': apellido,
            'nacionalidad': nacionalidad,
            'fecha_nacimiento': fecha_nacimiento
        }
        
        query = """UPDATE autores SET 
                    nombre = %(nombre)s, 
                    apellido = %(apellido)s,
                    nacionalidad = %(nacionalidad)s, 
                    fecha_nacimiento = %(fecha_nacimiento)s
                WHERE autor_id = %(autor_id)s"""
                
        self.postgres_pool.execute(query, data, commit=True)
        
        return {'result': 1, 'message': 'Autor actualizado con éxito'}

    def delete_autor(self, autor_id):
        # Verificar si el autor existe
        params = {'autor_id': autor_id}
        rv = self.postgres_pool.execute("SELECT autor_id FROM autores WHERE autor_id=%(autor_id)s AND activo=TRUE", params)
        
        if not rv:
            return {'error': 'Autor no encontrado o inactivo'}
        
        # Actualizar el campo activo en lugar de eliminar
        query = """UPDATE autores SET activo = FALSE WHERE autor_id = %(autor_id)s"""
        self.postgres_pool.execute(query, params, commit=True)
        
        return {'result': 1, 'message': 'Autor eliminado con éxito (desactivado)'}