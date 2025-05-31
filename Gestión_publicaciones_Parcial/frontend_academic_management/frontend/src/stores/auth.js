import { defineStore } from 'pinia'
import apiService from '../services/api' // ✅ Correcto

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user
  },

  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null
      
      try {
        const response = await apiService.post('/auth/login', credentials)
        const { access_token, refresh_token, user } = response.data
        
        this.token = access_token
        this.refreshToken = refresh_token
        this.user = user
        
        localStorage.setItem('token', access_token)
        localStorage.setItem('refreshToken', refresh_token)
        
        // Configurar token para futuras peticiones
        apiService.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        
        return { success: true }
      } catch (error) {
        this.error = error.response &&error.response.data && error.response.data.message || 'Error de autenticación'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async register(userData) {
      this.loading = true
      this.error = null
      
      try {
        await apiService.post('/auth/register', userData)
        return { success: true }
      } catch (error) {
        this.error = error.response &&error.response.data && error.response.data.message || 'Error en el registro'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async refreshAccessToken() {
      if (!this.refreshToken) return false
      
      try {
        const response = await apiService.post('/auth/refresh', {
          refresh_token: this.refreshToken
        })
        
        const { access_token } = response.data
        this.token = access_token
        localStorage.setItem('token', access_token)
        apiService.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        
        return true
      } catch (error) {
        this.logout()
        return false
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.refreshToken = null
      
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      delete apiService.defaults.headers.common['Authorization']
    },

    async initializeAuth() {
      if (this.token) {
        apiService.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        
        try {
          // Verificar que el token sigue siendo válido obteniendo el perfil del usuario
          const response = await apiService.get('/users/profile')
          this.user = response.data
        } catch (error) {
          // Si el token no es válido, intentar refrescar
          const refreshed = await this.refreshAccessToken()
          if (!refreshed) {
            this.logout()
          }
        }
      }
    }
  }
})