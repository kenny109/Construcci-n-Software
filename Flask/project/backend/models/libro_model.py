from project.backend.models.postgres_connection_pool import PostgreSQLPool

class LibroModel:
    def __init__(self):
        self.postgres_pool = PostgreSQLPool()

    def get_libro(self, libro_id):
        params = {'libro_id': libro_id}
        
        # Obtener información básica del libro
        rv = self.postgres_pool.execute("""
            SELECT libro_id, titulo, anio_publicacion
            FROM libros
            WHERE libro_id = %(libro_id)s AND activo = TRUE
        """, params)
        
        if not rv:
            return []
        
        libro = {
            'libro_id': rv[0][0],
            'titulo': rv[0][1],
            'anio_publicacion': rv[0][2],
            'autores': [],
            'generos': []
        }
        
        # Obtener autores del libro
        autores_rv = self.postgres_pool.execute("""
            SELECT a.autor_id, a.nombre, a.apellido
            FROM autores a
            INNER JOIN libro_autor la ON a.autor_id = la.autor_id
            WHERE la.libro_id = %(libro_id)s AND a.activo = TRUE
        """, params)
        
        for autor in autores_rv:
            libro['autores'].append({
                'autor_id': autor[0],
                'nombre': autor[1],
                'apellido': autor[2]
            })
        
        # Obtener géneros del libro
        generos_rv = self.postgres_pool.execute("""
            SELECT g.genero_id, g.nombre
            FROM generos g
            INNER JOIN libro_genero lg ON g.genero_id = lg.genero_id
            WHERE lg.libro_id = %(libro_id)s AND g.activo = TRUE
        """, params)
        
        for genero in generos_rv:
            libro['generos'].append({
                'genero_id': genero[0],
                'nombre': genero[1]
            })
        
        return [libro]

    def get_libros(self):
        # Obtener todos los libros activos
        rv = self.postgres_pool.execute("SELECT libro_id, titulo, anio_publicacion FROM libros WHERE activo = TRUE")
        
        data = []
        for result in rv:
            libro_id = result[0]
            libro = {
                'libro_id': libro_id,
                'titulo': result[1],
                'anio_publicacion': result[2],
                'autores': [],
                'generos': []
            }
            
            # Obtener autores para cada libro
            params = {'libro_id': libro_id}
            autores_rv = self.postgres_pool.execute("""
                SELECT a.autor_id, a.nombre, a.apellido
                FROM autores a
                INNER JOIN libro_autor la ON a.autor_id = la.autor_id
                WHERE la.libro_id = %(libro_id)s AND a.activo = TRUE
            """, params)
            
            for autor in autores_rv:
                libro['autores'].append({
                    'autor_id': autor[0],
                    'nombre': autor[1],
                    'apellido': autor[2]
                })
                
            # Obtener géneros para cada libro
            generos_rv = self.postgres_pool.execute("""
                SELECT g.genero_id, g.nombre
                FROM generos g
                INNER JOIN libro_genero lg ON g.genero_id = lg.genero_id
                WHERE lg.libro_id = %(libro_id)s AND g.activo = TRUE
            """, params)
            
            for genero in generos_rv:
                libro['generos'].append({
                    'genero_id': genero[0],
                    'nombre': genero[1]
                })
                
            data.append(libro)
        
        return data
    
    def get_autores_by_libro(self, libro_id):
        params = {'libro_id': libro_id}
        rv = self.postgres_pool.execute("""
            SELECT a.autor_id, a.nombre, a.apellido, a.nacionalidad, a.fecha_nacimiento
            FROM autores a
            INNER JOIN libro_autor la ON a.autor_id = la.autor_id
            WHERE la.libro_id = %(libro_id)s AND a.activo = TRUE
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

    def create_libro(self, titulo, anio_publicacion, autores_ids, generos_ids):
        # Validar que todos los autores existan
        for autor_id in autores_ids:
            params = {'autor_id': autor_id}
            rv = self.postgres_pool.execute("SELECT autor_id FROM autores WHERE autor_id = %(autor_id)s AND activo = TRUE", params)
            if not rv:
                return {'error': f'El autor con ID {autor_id} no existe o está inactivo'}
        
        # Validar que todos los géneros existan
        for genero_id in generos_ids:
            params = {'genero_id': genero_id}
            rv = self.postgres_pool.execute("SELECT genero_id FROM generos WHERE genero_id = %(genero_id)s AND activo = TRUE", params)
            if not rv:
                return {'error': f'El género con ID {genero_id} no existe o está inactivo'}
        
        # Insertar libro
        data = {
            'titulo': titulo,
            'anio_publicacion': anio_publicacion
        }
        
        query = """
            INSERT INTO libros (titulo, anio_publicacion)
            VALUES (%(titulo)s, %(anio_publicacion)s)
            RETURNING libro_id
        """
        
        libro_id = self.postgres_pool.execute(query, data, commit=True)
        
        # Insertar relaciones con autores
        for autor_id in autores_ids:
            data = {
                'libro_id': libro_id,
                'autor_id': autor_id
            }
            
            query = """
                INSERT INTO libro_autor (libro_id, autor_id)
                VALUES (%(libro_id)s, %(autor_id)s)
            """
            
            self.postgres_pool.execute(query, data, commit=True)
        
        # Insertar relaciones con géneros
        for genero_id in generos_ids:
            data = {
                'libro_id': libro_id,
                'genero_id': genero_id
            }
            
            query = """
                INSERT INTO libro_genero (libro_id, genero_id)
                VALUES (%(libro_id)s, %(genero_id)s)
            """
            
            self.postgres_pool.execute(query, data, commit=True)
        
        return {
            'libro_id': libro_id,
            'titulo': titulo,
            'anio_publicacion': anio_publicacion,
            'autores_ids': autores_ids,
            'generos_ids': generos_ids,
            'message': 'Libro creado con éxito'
        }

    def update_libro(self, libro_id, titulo, anio_publicacion, autores_ids, generos_ids):
        # Verificar si el libro existe
        params = {'libro_id': libro_id}
        rv = self.postgres_pool.execute("SELECT libro_id FROM libros WHERE libro_id = %(libro_id)s AND activo = TRUE", params)
        
        if not rv:
            return {'error': 'Libro no encontrado o inactivo'}
        
        # Validar que todos los autores existan
        for autor_id in autores_ids:
            params = {'autor_id': autor_id}
            rv = self.postgres_pool.execute("SELECT autor_id FROM autores WHERE autor_id = %(autor_id)s AND activo = TRUE", params)
            if not rv:
                return {'error': f'El autor con ID {autor_id} no existe o está inactivo'}
        
        # Validar que todos los géneros existan
        for genero_id in generos_ids:
            params = {'genero_id': genero_id}
            rv = self.postgres_pool.execute("SELECT genero_id FROM generos WHERE genero_id = %(genero_id)s AND activo = TRUE", params)
            if not rv:
                return {'error': f'El género con ID {genero_id} no existe o está inactivo'}
        
        # Actualizar libro
        data = {
            'libro_id': libro_id,
            'titulo': titulo,
            'anio_publicacion': anio_publicacion
        }
        
        query = """
            UPDATE libros
            SET titulo = %(titulo)s, anio_publicacion = %(anio_publicacion)s
            WHERE libro_id = %(libro_id)s
        """
        
        self.postgres_pool.execute(query, data, commit=True)
        
        # Eliminar relaciones antiguas con autores
        query = "DELETE FROM libro_autor WHERE libro_id = %(libro_id)s"
        self.postgres_pool.execute(query, {'libro_id': libro_id}, commit=True)
        
        # Insertar nuevas relaciones con autores
        for autor_id in autores_ids:
            data = {
                'libro_id': libro_id,
                'autor_id': autor_id
            }
            
            query = """
                INSERT INTO libro_autor (libro_id, autor_id)
                VALUES (%(libro_id)s, %(autor_id)s)
            """
            
            self.postgres_pool.execute(query, data, commit=True)
        
        # Eliminar relaciones antiguas con géneros
        query = "DELETE FROM libro_genero WHERE libro_id = %(libro_id)s"
        self.postgres_pool.execute(query, {'libro_id': libro_id}, commit=True)
        
        # Insertar nuevas relaciones con géneros
        for genero_id in generos_ids:
            data = {
                'libro_id': libro_id,
                'genero_id': genero_id
            }
            
            query = """
                INSERT INTO libro_genero (libro_id, genero_id)
                VALUES (%(libro_id)s, %(genero_id)s)
            """
            
            self.postgres_pool.execute(query, data, commit=True)
        
        return {
            'result': 1,
            'message': 'Libro actualizado con éxito'
        }

    def delete_libro(self, libro_id):
        # Verificar si el libro existe
        params = {'libro_id': libro_id}
        rv = self.postgres_pool.execute("SELECT libro_id FROM libros WHERE libro_id = %(libro_id)s AND activo = TRUE", params)
        
        if not rv:
            return {'error': 'Libro no encontrado o inactivo'}
        
        # Actualizar el campo activo en lugar de eliminar
        query = """UPDATE libros SET activo = FALSE WHERE libro_id = %(libro_id)s"""
        self.postgres_pool.execute(query, params, commit=True)
        
        return {'result': 1, 'message': 'Libro eliminado con éxito (desactivado)'}