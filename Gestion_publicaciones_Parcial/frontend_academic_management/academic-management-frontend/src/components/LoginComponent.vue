<!-- src/components/LoginComponent.vue -->
<template>
  <div class="login-container">
    <div class="login-card">
      <div class="tabs">
        <button 
          :class="['tab', { active: activeTab === 'login' }]"
          @click="activeTab = 'login'"
        >
          Iniciar Sesión
        </button>
        <button 
          :class="['tab', { active: activeTab === 'register' }]"
          @click="activeTab = 'register'"
        >
          Registrarse
        </button>
      </div>

      <!-- Login Form -->
      <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="form">
        <h2>Iniciar Sesión</h2>
        
        <div class="form-group">
          <label for="login-username">Nombre de Usuario:</label>
          <input
            id="login-username"
            v-model="loginForm.username"
            type="text"
            required
            placeholder="Ingrese su nombre de usuario"
          >
        </div>

        <div class="form-group">
          <label for="login-password">Contraseña:</label>
          <input
            id="login-password"
            v-model="loginForm.password"
            type="password"
            required
            placeholder="Ingrese su contraseña"
          >
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
        </button>
      </form>

      <!-- Register Form -->
      <form v-if="activeTab === 'register'" @submit.prevent="handleRegister" class="form">
        <h2>Registrarse</h2>
        
        <div class="form-row">
          <div class="form-group">
            <label for="register-firstname">Nombre:</label>
            <input
              id="register-firstname"
              v-model="registerForm.first_name"
              type="text"
              required
              placeholder="Nombre"
            >
          </div>
          
          <div class="form-group">
            <label for="register-lastname">Apellido:</label>
            <input
              id="register-lastname"
              v-model="registerForm.last_name"
              type="text"
              required
              placeholder="Apellido"
            >
          </div>
        </div>

        <div class="form-group">
          <label for="register-username">Usuario:</label>
          <input
            id="register-username"
            v-model="registerForm.username"
            type="text"
            required
            placeholder="Nombre de usuario"
          >
        </div>

        <div class="form-group">
          <label for="register-email">Email:</label>
          <input
            id="register-email"
            v-model="registerForm.email"
            type="email"
            required
            placeholder="correo@ejemplo.com"
          >
        </div>

        <div class="form-group">
          <label for="register-password">Contraseña:</label>
          <input
            id="register-password"
            v-model="registerForm.password"
            type="password"
            required
            placeholder="Contraseña"
          >
        </div>

        <div class="form-group">
          <label for="register-orcid">ORCID ID (opcional):</label>
          <input
            id="register-orcid"
            v-model="registerForm.orcid_id"
            type="text"
            placeholder="0000-0000-0000-0000"
          >
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Registrando...' : 'Registrarse' }}
        </button>
      </form>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-if="success" class="success-message">
        {{ success }}
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'LoginComponent',
  data() {
    return {
      activeTab: 'login',
      loading: false,
      error: '',
      success: '',
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        orcid_id: ''
      }
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      
      try {
        const result = await api.login(this.loginForm)
        this.success = 'Inicio de sesión exitoso'
        
        // Emit login event to parent
        this.$emit('login-success', result)
        
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async handleRegister() {
      this.loading = true
      this.error = ''
      this.success = ''
      
      try {
await api.register(this.registerForm)
        this.success = 'Registro exitoso. Ya puedes iniciar sesión.'
        
        // Reset form
        this.registerForm = {
          username: '',
          email: '',
          password: '',
          first_name: '',
          last_name: '',
          orcid_id: ''
        }
        
        // Switch to login tab
        setTimeout(() => {
          this.activeTab = 'login'
          this.success = ''
        }, 2000)
        
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    clearMessages() {
      this.error = ''
      this.success = ''
    }
  },
  watch: {
    activeTab() {
      this.clearMessages()
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.login-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 0;
  width: 100%;
  max-width: 400px;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #e0e0e0;
}

.tab {
  flex: 1;
  padding: 1rem;
  border: none;
  background: #f8f9fa;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab:first-child {
  border-radius: 8px 0 0 0;
}

.tab:last-child {
  border-radius: 0 8px 0 0;
}

.tab.active {
  background: white;
  border-bottom: 2px solid #007bff;
  color: #007bff;
}

.form {
  padding: 2rem;
}

.form h2 {
  margin: 0 0 1.5rem 0;
  text-align: center;
  color: #333;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1rem;
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  background-color: #0056b3;
}

.btn-primary:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  text-align: center;
}

.success-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #d1e7dd;
  color: #0f5132;
  border: 1px solid #badbcc;
  border-radius: 4px;
  text-align: center;
}
</style>