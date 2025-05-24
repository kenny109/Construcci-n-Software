<template>
  <div class="login-container">
    <div class="card login-card">
      <div class="card-header">
        <h2 class="card-title">📚 Biblioteca</h2>
        <p class="card-subtitle">Iniciar Sesión</p>
      </div>
      
      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>
      
      <form @submit.prevent="login">
        <div class="form-group">
          <label class="form-label">Usuario:</label>
          <input 
            v-model="credentials.username"
            type="text" 
            class="form-input"
            placeholder="Ingresa tu usuario"
            required
          >
        </div>
        
        <div class="form-group">
          <label class="form-label">Contraseña:</label>
          <input 
            v-model="credentials.password"
            type="password" 
            class="form-input"
            placeholder="Ingresa tu contraseña"
            required
          >
        </div>
        
        <button 
          type="submit" 
          class="btn btn-primary" 
          style="width: 100%;"
          :disabled="loading"
        >
          {{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
        </button>
      </form>
      
      <div class="login-links">
        <p>¿No tienes cuenta? 
          <router-link to="/register">Regístrate aquí</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'Login',
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      },
      error: '',
      loading: false
    }
  },
  methods: {
    async login() {
      if (!this.credentials.username || !this.credentials.password) {
        this.error = 'Por favor completa todos los campos'
        return
      }
      
      this.loading = true
      this.error = ''
      
      try {
        const response = await api.login(this.credentials)
        
        if (response.data.token) {
          localStorage.setItem('token', response.data.token)
          this.$router.push('/autores')
        } else {
          this.error = 'Error en el login'
        }
      } catch (error) {
        console.error('Error login:', error)
this.error = (error.response && error.response.data && error.response.data.error) || 
             (error.response && error.response.data && error.response.data.message) || 
             'Error al iniciar sesión'      } finally {
        this.loading = false
      }
    }
  }
}
</script>