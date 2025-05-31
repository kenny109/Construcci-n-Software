// src/services/auth.js
import apiClient from './api'

export const authService = {
  async login(credentials) {
    try {
      const response = await apiClient.post('/auth/login', credentials)
      const { access_token, refresh_token, user } = response.data
      
      // Guardar tokens en localStorage
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      localStorage.setItem('user', JSON.stringify(user))
      
      return { user, tokens: { access_token, refresh_token } }
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Error en el login')
    }
  },

  async register(userData) {
    try {
      const response = await apiClient.post('/auth/register', userData)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Error en el registro')
    }
  },

  async logout() {
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        await apiClient.post('/auth/logout', { refresh_token: refreshToken })
      }
    } catch (error) {
      console.error('Error during logout:', error)
    } finally {
      // Limpiar tokens independientemente del resultado
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    }
  },

  async getCurrentUser() {
    try {
      const response = await apiClient.get('/auth/me')
      return response.data
    } catch (error) {
      throw new Error('Error obteniendo información del usuario')
    }
  },

  isAuthenticated() {
    return !!localStorage.getItem('access_token')
  },

  getStoredUser() {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  }
}