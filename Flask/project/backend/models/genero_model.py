from project.backend.models.postgres_connection_pool import PostgreSQLPool

class GeneroModel:
    def __init__(self):
        self.postgres_pool = PostgreSQLPool()

    def get_genero(self, genero_id):
        params = {'genero_id': genero_id}
        rv = self.postgres_pool.execute("SELECT * FROM generos WHERE genero_id = %(genero_id)s AND activo = TRUE", params)
        
        data = []
        for result in rv:
            content = {
                'genero_id': result[0],
                'nombre': result[1]
            }
            data.append(content)
        
        return data

    def get_generos(self):
        rv = self.postgres_pool.execute("SELECT * FROM generos WHERE activo = TRUE")
        
        data = []
        for result in rv:
            content = {
                'genero_id': result[0],
                'nombre': result[1]
            }
            data.append(content)
        
        return data

    def create_genero(self, nombre):
        # Verificar si ya existe un género con el mismo nombre
        params = {'nombre': nombre}
        rv = self.postgres_pool.execute("SELECT genero_id FROM generos WHERE nombre = %(nombre)s", params)
        
        if rv:
            return {'error': 'Ya existe un género con ese nombre'}
        
        data = {'nombre': nombre}
        
        query = """
            INSERT INTO generos (nombre)
            VALUES (%(nombre)s)
            RETURNING genero_id
        """
        
        genero_id = self.postgres_pool.execute(query, data, commit=True)
        
        return {
            'genero_id': genero_id,
            'nombre': nombre,
            'message': 'Género creado con éxito'
        }

    def update_genero(self, genero_id, nombre):
        # Verificar si el género existe
        params = {'genero_id': genero_id}
        rv = self.postgres_pool.execute("SELECT genero_id FROM generos WHERE genero_id = %(genero_id)s AND activo = TRUE", params)
        
        if not rv:
            return {'error': 'Género no encontrado o inactivo'}
        
        # Verificar si ya existe otro género con el mismo nombre
        params = {'nombre': nombre, 'genero_id': genero_id}
        rv = self.postgres_pool.execute("""
            SELECT genero_id FROM generos 
            WHERE nombre = %(nombre)s AND genero_id != %(genero_id)s
        """, params)
        
        if rv:
            return {'error': 'Ya existe otro género con ese nombre'}
        
        data = {
            'genero_id': genero_id,
            'nombre': nombre
        }
        
        query = """
            UPDATE generos
            SET nombre = %(nombre)s
            WHERE genero_id = %(genero_id)s
        """
        
        self.postgres_pool.execute(query, data, commit=True)
        
        return {'result': 1, 'message': 'Género actualizado con éxito'}

    def delete_genero(self, genero_id):
        # Verificar si el género existe
        params = {'genero_id': genero_id}
        rv = self.postgres_pool.execute("SELECT genero_id FROM generos WHERE genero_id = %(genero_id)s AND activo = TRUE", params)
        
        if not rv:
            return {'error': 'Género no encontrado o inactivo'}
        
        # Actualizar el campo activo en lugar de eliminar
        query = """UPDATE generos SET activo = FALSE WHERE genero_id = %(genero_id)s"""
        self.postgres_pool.execute(query, params, commit=True)
        
        return {'result': 1, 'message': 'Género eliminado con éxito (desactivado)'}