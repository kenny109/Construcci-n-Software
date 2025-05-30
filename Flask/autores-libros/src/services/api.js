import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000'

// Crear instancia de axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para agregar token a las peticiones
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar respuestas
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default {
  // Auth endpoints
  login(credentials) {
    return api.post('/login', credentials)
  },
  
  register(userData) {
    return api.post('/register', userData)
  },

  // Autor endpoints
  getAutores() {
    return api.get('/autores')
  },

  getAutor(autorId) {
    return api.get('/autor', { autor_id: autorId })
  },

  createAutor(autorData) {
    return api.post('/autor', autorData)
  },

  updateAutor(autorData) {
    return api.put('/autor', autorData)
  },

  deleteAutor(autorId) {
    return api.delete('/autor', { data: { autor_id: autorId } })
  },

 getLibrosByAutor(autorId) {
  return api.get('/autor/libros', {
    params: { autor_id: autorId }  // Correcto: esto se convierte en ?autor_id=...
  })
}

,



  // Libro endpoints
  getLibros() {
    return api.get('/libros')
  },

  getLibro(libroId) {
    return api.get('/libro', { libro_id: libroId })
  },

  createLibro(libroData) {
    return api.post('/libro', libroData)
  },

  updateLibro(libroData) {
    return api.put('/libro', libroData)
  },

  deleteLibro(libroId) {
    return api.delete('/libro', { data: { libro_id: libroId } })
  },

  getAutoresByLibro(libroId) {
    return api.get('/libro/autores', { libro_id: libroId })
  },

  // Genero endpoints
  getGeneros() {
    return api.get('/generos')
  },

  getGenero(generoId) {
    return api.get('/genero', { genero_id: generoId })
  },

  createGenero(generoData) {
    return api.post('/genero', generoData)
  },

  updateGenero(generoData) {
    return api.put('/genero', generoData)
  },

  deleteGenero(generoId) {
    return api.delete('/genero', { data: { genero_id: generoId } })
  }
}