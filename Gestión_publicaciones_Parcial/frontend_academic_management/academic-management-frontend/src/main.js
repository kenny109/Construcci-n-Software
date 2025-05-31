import './assets/main.css'
//import './styles/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// Importar componentes globales
import LoadingSpinner from './components/common/LoadingSpinner.vue'
import BaseButton from './components/common/BaseButton.vue'
import BaseInput from './components/common/BaseInput.vue'
import BaseModal from './components/common/BaseModal.vue'

const app = createApp(App)

// Configurar Pinia para manejo de estado
app.use(createPinia())

// Configurar Vue Router
app.use(router)

// Registrar componentes globales
app.component('LoadingSpinner', LoadingSpinner)
app.component('BaseButton', BaseButton)
app.component('BaseInput', BaseInput)
app.component('BaseModal', BaseModal)

// Configuración global de propiedades
app.config.globalProperties.$appName = 'Academic Management System'

// Manejo global de errores
app.config.errorHandler = (err, vm, info) => {
  console.error('Error global capturado:', err, info)
  // Aquí podrías enviar el error a un servicio de logging
}

// Inicializar autenticación antes de montar la app
import { useAuthStore } from './stores/auth'

// Montar la aplicación
const appInstance = app.mount('#app')

// Inicializar el store de autenticación después de montar
const authStore = useAuthStore()
authStore.initializeAuth()

export default appInstance