import axios from 'axios'

class ApiService {
  constructor() {
    this.baseURL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api'
    this.token = localStorage.getItem('token')
    
    // Configure axios defaults
    axios.defaults.baseURL = this.baseURL
    axios.defaults.withCredentials = true

    if (this.token) {
      this.setAuthToken(this.token)
    }
    
    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.logout()
        }
        return Promise.reject(error)
      }
    )
  }

  setAuthToken(token) {
    this.token = token
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    localStorage.setItem('token', token)
  }

  removeAuthToken() {
    this.token = null
    delete axios.defaults.headers.common['Authorization']
    localStorage.removeItem('token')
  }

  logout() {
    this.removeAuthToken()
    localStorage.removeItem('user')
    window.location.reload()
  }

  // Authentication
  async login(credentials) {
    try {
      const response = await axios.post('/auth/login', credentials)
      const { access_token, user } = response.data
      
      this.setAuthToken(access_token)
      localStorage.setItem('user', JSON.stringify(user))
      
      return { token: access_token, user }
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al iniciar sesión')
    }
  }

  async register(userData) {
    try {
      const response = await axios.post('/auth/register', userData)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al registrar usuario')
    }
  }

  // Generic CRUD operations
  async getItems(endpoint, params = {}) {
    try {
      const response = await axios.get(`/${endpoint}`, { params })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al cargar datos')
    }
  }

  async getItem(endpoint, id) {
    try {
      const response = await axios.get(`/${endpoint}/${id}`)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al cargar elemento')
    }
  }

  async createItem(endpoint, data) {
    try {
      const response = await axios.post(`/${endpoint}`, data)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al crear elemento')
    }
  }

  async updateItem(endpoint, id, data) {
    try {
      const formCopy = { ...data }
      delete formCopy.id  // Quitar ID del cuerpo, ya va en la URL

      const response = await axios.put(`/${endpoint}/${id}`, formCopy)
      return response.data
    } catch (error) {
      console.error('Error del backend:', error.response?.data)
      throw new Error(error.response?.data?.error || 'Error al actualizar elemento')
    }
  }

  async deleteItem(endpoint, id) {
    try {
      const response = await axios.delete(`/${endpoint}/${id}`)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al eliminar elemento')
    }
  }

  // Specific methods for each entity
  
  // Countries
  async getCountries(params = {}) {
    return this.getItems('countries', params)
  }

  async createCountry(data) {
    return this.createItem('countries', data)
  }

  async updateCountry(id, data) {
    return this.updateItem('countries', id, data)
  }

  async deleteCountry(id) {
    return this.deleteItem('countries', id)
  }

  // Keywords
  async getKeywords(params = {}) {
    return this.getItems('keywords', params)
  }

  async createKeyword(data) {
    return this.createItem('keywords', data)
  }

  async updateKeyword(id, data) {
    return this.updateItem('keywords', id, data)
  }

  async deleteKeyword(id) {
    return this.deleteItem('keywords', id)
  }

  // Publication Types
  async getPublicationTypes(params = {}) {
    return this.getItems('publication-types', params)
  }

  async createPublicationType(data) {
    return this.createItem('publication-types', data)
  }

  async updatePublicationType(id, data) {
    return this.updateItem('publication-types', id, data)
  }

  async deletePublicationType(id) {
    return this.deleteItem('publication-types', id)
  }

  // Authors
  async getAuthors(params = {}) {
    return this.getItems('authors', params)
  }

  async createAuthor(data) {
    return this.createItem('authors', data)
  }

  async updateAuthor(id, data) {
    return this.updateItem('authors', id, data)
  }

  async deleteAuthor(id) {
    return this.deleteItem('authors', id)
  }

  // Journals
  async getJournals(params = {}) {
    return this.getItems('journals', params)
  }

  async createJournal(data) {
    return this.createItem('journals', data)
  }

  async updateJournal(id, data) {
    return this.updateItem('journals', id, data)
  }

  async deleteJournal(id) {
    return this.deleteItem('journals', id)
  }

  // Conferences
  async getConferences(params = {}) {
    return this.getItems('conferences', params)
  }

  async createConference(data) {
    return this.createItem('conferences', data)
  }

  async updateConference(id, data) {
    return this.updateItem('conferences', id, data)
  }

  async deleteConference(id) {
    return this.deleteItem('conferences', id)
  }

  // Publications
  async getPublications(params = {}) {
    return this.getItems('publications', params)
  }

  async getPublication(id) {
    return this.getItem('publications', id)
  }

  async createPublication(data) {
    return this.createItem('publications', data)
  }

  async updatePublication(id, data) {
    return this.updateItem('publications', id, data)
  }

  async deletePublication(id) {
    return this.deleteItem('publications', id)
  }

  // Projects
  async getProjects(params = {}) {
    return this.getItems('projects', params)
  }

  async createProject(data) {
    return this.createItem('projects', data)
  }

  async updateProject(id, data) {
    return this.updateItem('projects', id, data)
  }

  async deleteProject(id) {
    return this.deleteItem('projects', id)
  }
  async addAuthorToPublication(publicationId, authorData) {
  const response = await axios.post(`/publication-authors/${publicationId}/authors`, authorData)
  return response.data
}

}

export default new ApiService()