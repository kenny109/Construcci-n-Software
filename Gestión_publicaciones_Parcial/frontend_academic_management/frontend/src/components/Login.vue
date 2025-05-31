<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>Academic Management</h1>
        <p>Inicia sesión en tu cuenta</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div v-if="error" class="alert alert-error">
          {{ error }}
        </div>
        
        <div class="form-group">
          <label for="username" class="form-label">Usuario</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            class="form-control"
            required
            placeholder="Ingresa tu usuario"
          >
        </div>
        
        <div class="form-group">
          <label for="password" class="form-label">Contraseña</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="form-control"
            required
            placeholder="Ingresa tu contraseña"
          >
        </div>
        
        <button
          type="submit"
          class="btn btn-primary btn-login"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
        </button>
      </form>
      
      <div class="login-footer">
        <p>¿No tienes cuenta? <a href="#" @click="showRegister = true">Regístrate</a></p>
      </div>
    </div>
    
    <!-- Modal de Registro -->
    <div v-if="showRegister" class="modal-overlay" @click="closeRegister">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">Crear Cuenta</h3>
          <button @click="closeRegister" class="btn-close">&times;</button>
        </div>
        
        <form @submit.prevent="handleRegister">
          <div v-if="registerError" class="alert alert-error">
            {{ registerError }}
          </div>
          
          <div class="form-group">
            <label class="form-label">Usuario</label>
            <input
              v-model="registerForm.username"
              type="text"
              class="form-control"
              required
              placeholder="Usuario"
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Email</label>
            <input
              v-model="registerForm.email"
              type="email"
              class="form-control"
              required
              placeholder="Email"
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Nombre</label>
            <input
              v-model="registerForm.first_name"
              type="text"
              class="form-control"
              required
              placeholder="Nombre"
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Apellido</label>
            <input
              v-model="registerForm.last_name"
              type="text"
              class="form-control"
              required
              placeholder="Apellido"
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Contraseña</label>
            <input
              v-model="registerForm.password"
              type="password"
              class="form-control"
              required
              placeholder="Contraseña"
            >
          </div>
          
          <div class="modal-actions">
            <button type="button" @click="closeRegister" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary" :disabled="isRegistering">
              {{ isRegistering ? 'Creando...' : 'Crear Cuenta' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const form = ref({
      username: '',
      password: ''
    })
    
    const registerForm = ref({
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      password: ''
    })
    
    const showRegister = ref(false)
    const registerError = ref('')
    const isRegistering = ref(false)
    
    const isLoading = computed(() => authStore.isLoading)
    const error = computed(() => authStore.error)
    
    const handleLogin = async () => {
      try {
        await authStore.login(form.value)
        router.push('/dashboard')
      } catch (error) {
        console.error('Login error:', error)
      }
    }
    
    const handleRegister = async () => {
      isRegistering.value = true
      registerError.value = ''
      
      try {
        await authStore.register(registerForm.value)
        showRegister.value = false
        registerForm.value = {
          username: '',
          email: '',
          first_name: '',
          last_name: '',
          password: ''
        }
        alert('Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
      } catch (error) {
        registerError.value = error.message
      } finally {
        isRegistering.value = false
      }
    }
    
    const closeRegister = () => {
      showRegister.value = false
      registerError.value = ''
      registerForm.value = {
        username: '',
        email: '',
        first_name: '',
        last_name: '',
        password: ''
      }
    }
    
    onMounted(() => {
      authStore.initializeAuth()
    })
    
    return {
      form,
      registerForm,
      showRegister,
      registerError,
      isRegistering,
      isLoading,
      error,
      handleLogin,
      handleRegister,
      closeRegister
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
  padding: 2rem;
}

.login-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
  padding: 3rem;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.5rem;
}

.login-header p {
  color: #666;
  font-size: 1rem;
}

.login-form {
  margin-bottom: 2rem;
}

.btn-login {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: 600;
}

.login-footer {
  text-align: center;
}

.login-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.login-footer a:hover {
  text-decoration: underline;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}
</style>