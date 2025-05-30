<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>Sistema de Gestión de Publicaciones</h1>
        <p>Ingrese sus credenciales para acceder</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>
        
        <div class="form-group">
          <label for="username" class="form-label">Usuario</label>
          <input
            id="username"
            v-model="credentials.username"
            type="text"
            class="form-input"
            placeholder="Ingrese su usuario"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="password" class="form-label">Contraseña</label>
          <input
            id="password"
            v-model="credentials.password"
            type="password"
            class="form-input"
            placeholder="Ingrese su contraseña"
            required
          />
        </div>
        
        <button
          type="submit"
          :disabled="loading"
          class="btn btn-primary login-btn"
        >
          <span v-if="loading" class="spinner"></span>
          {{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
        </button>
      </form>
      
      <div class="login-footer">
        <p><strong>Usuarios de prueba:</strong></p>
        <ul>
          <li>admin / admin123</li>
          <li>user / user123</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const credentials = ref({
      username: '',
      password: ''
    })
    
    const loading = ref(false)
    const error = ref('')
    
    const handleLogin = async () => {
      loading.value = true
      error.value = ''
      
      const result = await authStore.login(credentials.value)
      
      if (result.success) {
        router.push('/dashboard')
      } else {
        error.value = result.message
      }
      
      loading.value = false
    }
    
    return {
      credentials,
      loading,
      error,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #1f2937;
}

.login-header p {
  color: #6b7280;
  font-size: 0.9rem;
}

.login-form {
  margin-bottom: 1.5rem;
}

.login-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.login-footer p {
  font-size: 0.8rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.login-footer ul {
  list-style: none;
  font-size: 0.8rem;
  color: #374151;
}

.login-footer li {
  margin-bottom: 0.25rem;
  font-family: monospace;
  background-color: #f3f4f6;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  display: inline-block;
  margin-right: 0.5rem;
}
</style>