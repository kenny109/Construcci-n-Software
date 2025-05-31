const API_BASE_URL = 'http://localhost:5000/api'

class ApiService {
  constructor() {
    this.token = localStorage.getItem('token')
  }

  setToken(token) {
    this.token = token
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json'
    }
    
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }
    
    return headers
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    const config = {
      headers: this.getHeaders(),
      ...options
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // Auth endpoints
  async login(credentials) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials)
    })
  }

  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    })
  }

  // Authors endpoints
  async getAuthors() {
    return this.request('/authors')
  }

  async getAuthor(id) {
    return this.request(`/authors/${id}`)
  }

  async createAuthor(authorData) {
    return this.request('/authors', {
      method: 'POST',
      body: JSON.stringify(authorData)
    })
  }

  async updateAuthor(id, authorData) {
    return this.request(`/authors/${id}`, {
      method: 'PUT',
      body: JSON.stringify(authorData)
    })
  }

  async deleteAuthor(id) {
    return this.request(`/authors/${id}`, {
      method: 'DELETE'
    })
  }

  // Publications endpoints
  async getPublications() {
    return this.request('/publications')
  }

  async getPublication(id) {
    return this.request(`/publications/${id}`)
  }

  async createPublication(publicationData) {
    return this.request('/publications', {
      method: 'POST',
      body: JSON.stringify(publicationData)
    })
  }

  async updatePublication(id, publicationData) {
    return this.request(`/publications/${id}`, {
      method: 'PUT',
      body: JSON.stringify(publicationData)
    })
  }

  async deletePublication(id) {
    return this.request(`/publications/${id}`, {
      method: 'DELETE'
    })
  }

  // Users endpoints
  async getUsers() {
    return this.request('/users')
  }

  async getUser(id) {
    return this.request(`/users/${id}`)
  }

  async createUser(userData) {
    return this.request('/users', {
      method: 'POST',
      body: JSON.stringify(userData)
    })
  }

  async updateUser(id, userData) {
    return this.request(`/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(userData)
    })
  }

  async deleteUser(id) {
    return this.request(`/users/${id}`, {
      method: 'DELETE'
    })
  }

  // Publication Types endpoints
  async getPublicationTypes() {
    return this.request('/publication-types')
  }

  // Journals endpoints
  async getJournals() {
    return this.request('/journals')
  }

  // Conferences endpoints
  async getConferences() {
    return this.request('/conferences')
  }
}

export default new ApiService()