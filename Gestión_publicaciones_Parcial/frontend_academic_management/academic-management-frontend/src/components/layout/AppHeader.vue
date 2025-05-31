<!-- src/components/layout/AppHeader.vue -->
<template>
  <header class="app-header">
    <div class="header-content">
      <!-- Logo y Título -->
      <div class="header-left">
        <div class="logo-container">
          <h1 class="app-title">Academic Management</h1>
        </div>
      </div>

      <!-- Centro - Breadcrumb o título de sección -->
      <div class="header-center">
        <div class="breadcrumb">
          <span class="breadcrumb-item">{{ currentPageTitle }}</span>
        </div>
      </div>

      <!-- Derecha - Usuario y acciones -->
      <div class="header-right">
        <!-- Notificaciones -->
        <button class="header-btn notification-btn" title="Notificaciones">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
          <span v-if="notificationCount > 0" class="notification-badge">{{ notificationCount }}</span>
        </button>

        <!-- Perfil de usuario -->
        <div class="user-menu" @click="toggleUserMenu" v-click-outside="closeUserMenu">
          <div class="user-info">
            <div class="user-avatar">
              {{ userInitials }}
            </div>
            <div class="user-details">
              <span class="user-name">{{ user?.first_name }} {{ user?.last_name }}</span>
              <span class="user-role">{{ user?.role }}</span>
            </div>
            <svg 
              class="dropdown-arrow" 
              :class="{ 'rotated': isUserMenuOpen }"
              width="16" 
              height="16" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              stroke-width="2"
            >
              <path d="M6 9l6 6 6-6"></path>
            </svg>
          </div>

          <!-- Dropdown del usuario -->
          <div v-if="isUserMenuOpen" class="user-dropdown">
            <div class="dropdown-header">
              <div class="user-avatar large">{{ userInitials }}</div>
              <div class="user-info-detailed">
                <p class="user-full-name">{{ user?.first_name }} {{ user?.last_name }}</p>
                <p class="user-email">{{ user?.email }}</p>
              </div>
            </div>
            
            <div class="dropdown-divider"></div>
            
            <div class="dropdown-menu">
              <button class="dropdown-item" @click="goToProfile">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                Mi Perfil
              </button>
              
              <button class="dropdown-item" @click="goToSettings">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="3"></circle>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                </svg>
                Configuración
              </button>
            </div>
            
            <div class="dropdown-divider"></div>
            
            <button class="dropdown-item logout-item" @click="handleLogout">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16,17 21,12 16,7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// Estado local
const isUserMenuOpen = ref(false)
const notificationCount = ref(3) // Ejemplo

// Computed
const user = computed(() => authStore.user)

const userInitials = computed(() => {
  if (!user.value) return 'U'
  const first = user.value.first_name?.charAt(0) || ''
  const last = user.value.last_name?.charAt(0) || ''
  return (first + last).toUpperCase() || user.value.username?.charAt(0).toUpperCase() || 'U'
})

const currentPageTitle = computed(() => {
  const routeNames = {
    'Dashboard': 'Panel de Control',
    'Countries': 'Países',
    'Keywords': 'Palabras Clave',
    'PublicationTypes': 'Tipos de Publicación'
  }
  return routeNames[route.name] || 'Academic Management'
})

// Métodos
const toggleUserMenu = () => {
  isUserMenuOpen.value = !isUserMenuOpen.value
}

const closeUserMenu = () => {
  isUserMenuOpen.value = false
}

const goToProfile = () => {
  closeUserMenu()
  // router.push('/profile')
  console.log('Ir a perfil')
}

const goToSettings = () => {
  closeUserMenu()
  // router.push('/settings')
  console.log('Ir a configuración')
}

const handleLogout = async () => {
  closeUserMenu()
  try {
    await authStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('Error during logout:', error)
  }
}

// Directiva personalizada para click fuera
const vClickOutside = {
  beforeMount(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value()
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent)
  }
}
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1000;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 64px;
  max-width: 1400px;
  margin: 0 auto;
}

.header-left {
  display: flex;
  align-items: center;
}

.app-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: white;
}

.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}

.breadcrumb-item {
  font-size: 16px;
  font-weight: 500;
  opacity: 0.9;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.2s;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.notification-badge {
  position: absolute;
  top: 2px;
  right: 2px;
  background-color: #ef4444;
  color: white;
  font-size: 10px;
  font-weight: bold;
  border-radius: 50%;
  min-width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.user-menu {
  position: relative;
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 12px;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.user-info:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  color: white;
}

.user-avatar.large {
  width: 48px;
  height: 48px;
  font-size: 18px;
}

.user-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  line-height: 1.2;
}

.user-role {
  font-size: 12px;
  opacity: 0.8;
  text-transform: capitalize;
  line-height: 1.2;
}

.dropdown-arrow {
  transition: transform 0.2s;
}

.dropdown-arrow.rotated {
  transform: rotate(180deg);
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  min-width: 280px;
  z-index: 1001;
  color: #374151;
  border: 1px solid #e5e7eb;
}

.dropdown-header {
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info-detailed {
  flex: 1;
}

.user-full-name {
  font-weight: 600;
  margin: 0 0 4px 0;
  color: #111827;
}

.user-email {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.dropdown-divider {
  height: 1px;
  background-color: #e5e7eb;
  margin: 0;
}

.dropdown-menu {
  padding: 8px 0;
}

.dropdown-item {
  width: 100%;
  padding: 12px 16px;
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #374151;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: #f3f4f6;
}

.logout-item {
  color: #dc2626;
}

.logout-item:hover {
  background-color: #fef2f2;
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    padding: 0 16px;
  }
  
  .header-center {
    display: none;
  }
  
  .user-details {
    display: none;
  }
  
  .user-dropdown {
    min-width: 240px;
  }
}
</style>