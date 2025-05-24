<template>
  <div class="login-container">
    <div class="card login-card">
      <div class="card-header">
        <h2 class="card-title">📚 Biblioteca</h2>
        <p class="card-subtitle">Crear Cuenta</p>
      </div>
      
      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>
      
      <div v-if="success" class="alert alert-success">
        {{ success }}
      </div>
      
      <form @submit.prevent="register">
        <div class="form-group">
          <label class="form-label">Usuario:</label>
          <input 
            v-model="userData.username"
            type="text" 
            class="form-input"
            placeholder="Elige un nombre de usuario"
            minlength="3"
            required
          >
        </div>
        
        <div class="form-group">
          <label class="form-label">Contraseña:</label>
          <input 
            v-model="userData.password"
            type="password" 
            class="form-input"
            placeholder="Crea una contraseña segura"
            minlength="6"
            required
          >
        </div>
        
        <div class="form-group">
          <label class="form-label">Confirmar Contraseña:</label>
          <input 
            v-model="confirmPassword"
            type="password" 
            class="form-input"
            placeholder="Confirma tu contraseña"
            required
          >
        </div>
        
        <button 
          type="submit" 
          class="btn btn-success" 
          style="width: 100%;"
          :disabled="loading"
        >
          {{ loading ? 'Registrando...' : 'Crear Cuenta' }}
        </button>
      </form>
      
      <div class="login-links">
        <p>¿Ya tienes cuenta? 
          <router-link to="/login">Inicia sesión aquí</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'Register',
  data() {
    return {
      userData: {
        username: '',
        password: ''
      },
      confirmPassword: '',
      error: '',
      success: '',
      loading: false
    }
  },
  methods: {
    async register() {
      // Validaciones
      if (!this.userData.username || !this.userData.password || !this.confirmPassword) {
        this.error = 'Por favor completa todos los campos'
        return
      }
      
      if (this.userData.username.length < 3) {
        this.error = 'El usuario debe tener al menos 3 caracteres'
        return
      }
      
      if (this.userData.password.length < 6) {
        this.error = 'La contraseña debe tener al menos 6 caracteres'
        return
      }
      
      if (this.userData.password !== this.confirmPassword) {
        this.error = 'Las contraseñas no coinciden'
        return
      }
      
      this.loading = true
      this.error = ''
      this.success = ''
      
      try {
        const response = await api.register(this.userData)
        
        if (response.data.message) {
          this.success = 'Usuario registrado con éxito. Puedes iniciar sesión ahora.'
          // Limpiar formulario
          this.userData = { username: '', password: '' }
          this.confirmPassword = ''
          
          // Redirigir después de 2 segundos
          setTimeout(() => {
            this.$router.push('/login')
          }, 2000)
        }
      } catch (error) {
        console.error('Error registro:', error)
this.error = (error.response && error.response.data && error.response.data.error) || 
             (error.response && error.response.data && error.response.data.message) || 
             'Error al registrar usuario'      } finally {
        this.loading = false
      }
    }
  }
}
</script>