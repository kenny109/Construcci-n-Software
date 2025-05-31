<template>
  <div id="app">
    <!-- Mostrar layout completo solo si está autenticado -->
    <AppLayout v-if="isAuthenticated">
      <RouterView />
    </AppLayout>
    
    <!-- Mostrar solo el contenido sin layout para páginas públicas -->
    <div v-else class="public-layout">
      <RouterView />
    </div>
    
    <!-- Loading global -->
    <div v-if="isLoading" class="global-loading">
      <LoadingSpinner size="large" />
      <p>Cargando...</p>
    </div>
    
    <!-- Notification toast -->
    <div 
      v-if="notification.show" 
      class="notification-toast"
      :class="[`notification-${notification.type}`]"
    >
      <div class="notification-content">
        <span>{{ notification.message }}</span>
        <button @click="hideNotification" class="notification-close">×</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'
import AppLayout from './components/layout/AppLayout.vue'

// Store de autenticación
const authStore = useAuthStore()

// Estado reactivo para notificaciones
const notification = reactive({
  show: false,
  message: '',
  type: 'info', // info, success, warning, error
  timeout: null
})

// Computed properties
const isAuthenticated = computed(() => authStore.isAuthenticated)
const isLoading = computed(() => authStore.loading)

// Funciones para manejo de notificaciones
const showNotification = (message, type = 'info', duration = 4000) => {
  // Limpiar timeout anterior si existe
  if (notification.timeout) {
    clearTimeout(notification.timeout)
  }
  
  notification.message = message
  notification.type = type
  notification.show = true
  
  // Auto-ocultar después del tiempo especificado
  notification.timeout = setTimeout(() => {
    hideNotification()
  }, duration)
}

const hideNotification = () => {
  notification.show = false
  notification.message = ''
  if (notification.timeout) {
    clearTimeout(notification.timeout)
    notification.timeout = null
  }
}

// Función global para mostrar notificaciones (accesible desde cualquier componente)
const globalNotify = {
  success: (message, duration) => showNotification(message, 'success', duration),
  error: (message, duration) => showNotification(message, 'error', duration),
  warning: (message, duration) => showNotification(message, 'warning', duration),
  info: (message, duration) => showNotification(message, 'info', duration)
}

// Hacer la función global disponible
import { getCurrentInstance } from 'vue'
const app = getCurrentInstance()
if (app) {
  app.appContext.config.globalProperties.$notify = globalNotify
}

// Lifecycle hooks
onMounted(() => {
  // Cualquier inicialización adicional
  console.log('Academic Management System iniciado')
})

// Manejo de errores no capturados
window.addEventListener('unhandledrejection', (event) => {
  console.error('Error no manejado:', event.reason)
  showNotification('Ha ocurrido un error inesperado', 'error')
})
</script>

<style>
/* Estilos globales de la aplicación */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--color-text);
  background-color: var(--color-background);
  min-height: 100vh;
}

/* Layout para páginas públicas */
.public-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Loading global */
.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.global-loading p {
  margin-top: 1rem;
  font-size: 1.1rem;
  color: var(--color-text-muted);
}

/* Notificaciones toast */
.notification-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10000;
  min-width: 300px;
  max-width: 500px;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  animation: slideInRight 0.3s ease-out;
}

.notification-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.notification-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.notification-close:hover {
  opacity: 1;
}

/* Tipos de notificación */
.notification-success {
  background-color: #d4edda;
  color: #155724;
  border-left: 4px solid #28a745;
}

.notification-error {
  background-color: #f8d7da;
  color: #721c24;
  border-left: 4px solid #dc3545;
}

.notification-warning {
  background-color: #fff3cd;
  color: #856404;
  border-left: 4px solid #ffc107;
}

.notification-info {
  background-color: #d1ecf1;
  color: #0c5460;
  border-left: 4px solid #17a2b8;
}

/* Animaciones */
@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Variables CSS para theming */
:root {
  --color-background: #ffffff;
  --color-background-soft: #f8f9fa;
  --color-background-mute: #f2f3f4;
  
  --color-border: #ddd;
  --color-border-hover: #c4c4c4;
  
  --color-heading: #2c3e50;
  --color-text: #2c3e50;
  --color-text-muted: #6c757d;
  
  --color-primary: #007bff;
  --color-primary-hover: #0056b3;
  --color-success: #28a745;
  --color-danger: #dc3545;
  --color-warning: #ffc107;
  --color-info: #17a2b8;
  
  --section-gap: 160px;
}

/* Responsive design */
@media (max-width: 768px) {
  .notification-toast {
    top: 10px;
    right: 10px;
    left: 10px;
    min-width: auto;
  }
}

/* Utilidades comunes */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }
.mt-1 { margin-top: 0.25rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-3 { margin-top: 1rem; }
.mt-4 { margin-top: 1.5rem; }
.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-3 { margin-bottom: 1rem; }
.mb-4 { margin-bottom: 1.5rem; }
.ml-1 { margin-left: 0.25rem; }
.ml-2 { margin-left: 0.5rem; }
.mr-1 { margin-right: 0.25rem; }
.mr-2 { margin-right: 0.5rem; }
</style>