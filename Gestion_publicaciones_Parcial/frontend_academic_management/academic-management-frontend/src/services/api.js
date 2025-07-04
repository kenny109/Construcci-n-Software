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

  // ORCID methods
  async checkOrcidService() {
    try {
      const response = await axios.get('/orcid/')
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al verificar el servicio ORCID')
    }
  }

  async getOrcidResearcher(orcidId) {
    try {
      const response = await axios.get(`/orcid/researcher/${orcidId}`)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al obtener información del investigador')
    }
  }

  async getOrcidWorks(orcidId) {
    try {
      const response = await axios.get(`/orcid/researcher/${orcidId}/works`)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al obtener las publicaciones del investigador')
    }
  }

  async syncOrcidResearcher(orcidId) {
    try {
      const response = await axios.post(`/orcid/sync/${orcidId}`)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al sincronizar datos del investigador')
    }
  }

  // Nuevas funciones añadidas desde orcid.py
  
  /**
   * Crea una publicación en la base de datos a partir de datos de ORCID
   * @param {Object} publicationData - Datos de la publicación
   * @param {string} publicationData.title - Título de la publicación (obligatorio)
   * @param {string} publicationData.type - Tipo de publicación
   * @param {string} publicationData.journal - Nombre del journal
   * @param {number} publicationData.year - Año de publicación
   * @param {string} publicationData.external_id - ID externo
   * @param {string} publicationData.doi - DOI de la publicación
   * @param {string} publicationData.url - URL de la publicación
   * @param {string} publicationData.abstract - Resumen de la publicación
   * @param {string} publicationData.pdf_url - URL del PDF
   * @param {number} publicationData.month - Mes de publicación
   * @param {number} publicationData.day - Día de publicación
   * @returns {Promise<Object>} - Respuesta con la publicación creada
   */
  async createPublicationFromOrcid(publicationData) {
    try {
      const response = await axios.post('/orcid/publications', publicationData)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al crear publicación desde ORCID')
    }
  }

  /**
   * Crea múltiples publicaciones en lote desde datos de ORCID
   * @param {Array} publicationsArray - Array de objetos con datos de publicaciones
   * @returns {Promise<Object>} - Respuesta con las publicaciones creadas y errores
   */
  async createPublicationsBatch(publicationsArray) {
    try {
      const response = await axios.post('/orcid/publications/batch', {
        publications: publicationsArray
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al crear publicaciones en lote')
    }
  }

  /**
   * Método auxiliar para importar publicaciones desde ORCID
   * Este método combina la obtención de trabajos y la creación en lote
   * @param {string} orcidId - ID de ORCID del investigador
   * @returns {Promise<Object>} - Respuesta con el resultado de la importación
   */
  async importPublicationsFromOrcid(orcidId) {
    try {
      // Primero obtenemos los trabajos del investigador
      const worksResponse = await this.getOrcidWorks(orcidId)
      
      if (!worksResponse.success || !worksResponse.data || worksResponse.data.length === 0) {
        throw new Error('No se encontraron publicaciones para importar')
      }

      // Luego las creamos en lote
      const batchResponse = await this.createPublicationsBatch(worksResponse.data)
      
      return {
        success: true,
        message: `Importación completada desde ORCID: ${orcidId}`,
        totalWorks: worksResponse.count,
        createdPublications: batchResponse.created?.length || 0,
        errors: batchResponse.errors || [],
        details: batchResponse
      }
    } catch (error) {
      throw new Error(error.message || 'Error al importar publicaciones desde ORCID')
    }
  }

  /**
   * Método auxiliar para crear una publicación individual desde datos de ORCID
   * con validación adicional
   * @param {Object} orcidWorkData - Datos del trabajo desde ORCID
   * @returns {Promise<Object>} - Respuesta con la publicación creada
   */
  async createSinglePublicationFromOrcid(orcidWorkData) {
    try {
      // Validación básica
      if (!orcidWorkData.title) {
        throw new Error('El título es obligatorio para crear una publicación')
      }

      // Preparar los datos para el backend
      const publicationData = {
        title: orcidWorkData.title,
        type: orcidWorkData.type || 'journal-article',
        journal: orcidWorkData.journal || '',
        year: orcidWorkData.year,
        external_id: orcidWorkData.external_id,
        doi: orcidWorkData.doi,
        url: orcidWorkData.url
      }

      return await this.createPublicationFromOrcid(publicationData)
    } catch (error) {
      throw new Error(error.message || 'Error al crear publicación individual desde ORCID')
    }
  }
  async fetchAuthorFromOrcid(orcidId) {
  const response = await fetch(`${this.baseURL}/orcid/fetch-from-orcid`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('token')}`
    },
    body: JSON.stringify({ orcid_id: orcidId })
  });
  return await response.json();
}

async getPublicationsCount() {
  try {
    const response = await axios.get('/api/publications/count', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Error al obtener el conteo de publicaciones');
  }
}

}

export default new ApiService()