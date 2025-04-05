from project.backend.models.postgres_connection_pool import PostgreSQLPool
class LibroModel:
    def __init__(self):
        self.postgres_pool = PostgreSQLPool()

    def get_libro(self, libro_id):
        params = {'libro_id': libro_id}
        rv = self.postgres_pool.execute("""
            SELECT L.libro_id, L.titulo, L.genero, L.anio_publicacion, A.nombre, A.apellido
            FROM libros L
            INNER JOIN autores A ON L.autor_id = A.autor_id
            WHERE L.libro_id = %(libro_id)s
        """, params)

        data = []
        content = {}
        for result in rv:
            content = {
                'libro_id': result[0],
                'titulo': result[1],
                'genero': result[2],
                'anio_publicacion': result[3],
                'nombre_autor': result[4],
                'apellido_autor': result[5]
            }
            data.append(content)
            content = {}
        return data

    def get_libros(self):
        rv = self.postgres_pool.execute("""
            SELECT L.libro_id, L.titulo, L.genero, L.anio_publicacion, A.nombre, A.apellido
            FROM libros L
            INNER JOIN autores A ON L.autor_id = A.autor_id
        """)

        data = []
        content = {}
        for result in rv:
            content = {
                'libro_id': result[0],
                'titulo': result[1],
                'genero': result[2],
                'anio_publicacion': result[3],
                'nombre_autor': result[4],
                'apellido_autor': result[5]
            }
            data.append(content)
            content = {}
        return data

    def create_libro(self, titulo, genero, anio_publicacion, autor_id):
        data = {
            'titulo': titulo,
            'genero': genero,
            'anio_publicacion': anio_publicacion,
            'autor_id': autor_id
        }

        query = """
            INSERT INTO libros (titulo, genero, anio_publicacion, autor_id)
            VALUES (%(titulo)s, %(genero)s, %(anio_publicacion)s, %(autor_id)s)
            RETURNING libro_id
        """

        cursor = self.postgres_pool.execute(query, data, commit=True)
        data['libro_id'] = cursor.lastrowid
        return data
    def update_libro(self, libro_id, titulo, genero, anio_publicacion, autor_id):
        data = {
            'libro_id': libro_id,
            'titulo': titulo,
            'genero': genero,
            'anio_publicacion': anio_publicacion,
            'autor_id': autor_id
        }

        query = """
            UPDATE libros
            SET titulo = %(titulo)s, genero = %(genero)s, anio_publicacion = %(anio_publicacion)s, autor_id = %(autor_id)s
            WHERE libro_id = %(libro_id)s
        """

        self.postgres_pool.execute(query, data, commit=True)

        return {'result': 1}

    def delete_libro(self, libro_id):
        params = {'libro_id': libro_id}

        query = """DELETE FROM libros WHERE libro_id = %(libro_id)s"""
        self.postgres_pool.execute(query, params, commit=True)

        data = {'result': 1}
        return data


if __name__ == "__main__":
    lm = LibroModel()
    print(lm.create_libro('Nuevo libro desde python', 'Ficción', 2024, 1))
