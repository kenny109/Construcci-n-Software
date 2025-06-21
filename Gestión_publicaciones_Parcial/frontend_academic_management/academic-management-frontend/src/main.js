import { createApp } from 'vue'
import App from './App.vue'
import './styles/global.css'

// Crear la aplicación
const app = createApp(App)

// Configuración global para manejar errores
app.config.errorHandler = (error, instance, info) => {
  console.error('Error en la aplicación:', error)
  console.error('Información del error:', info)
}

// Propiedades globales disponibles en todos los componentes
app.config.globalProperties.$formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

app.config.globalProperties.$formatDateTime = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString('es-ES', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Montar la aplicación
app.mount('#app')