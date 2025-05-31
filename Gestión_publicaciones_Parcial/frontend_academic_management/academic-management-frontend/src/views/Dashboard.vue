<template>
  <div class="app-layout">
    <!-- Sidebar -->
    <nav class="sidebar" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo">
          <h2 v-if="!sidebarCollapsed">Academic Mgmt</h2>
          <h2 v-else>AM</h2>
        </div>
        <button @click="toggleSidebar" class="toggle-btn">
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path fill="currentColor" d="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z"/>
          </svg>
        </button>
      </div>

      <div class="sidebar-content">
        <ul class="nav-menu">
          <li>
            <router-link to="/dashboard" class="nav-item">
              <svg class="nav-icon" viewBox="0 0 24 24">
                <path fill="currentColor" d="M13,3V9H21V3M13,21H21V11H13M3,21H11V15H3M3,13H11V3H3V13Z"/>
              </svg>
              <span v-if="!sidebarCollapsed">Dashboard</span>
            </router-link>
          </li>
          <li>
            <router-link to="/countries" class="nav-item">
              <svg class="nav-icon" viewBox="0 0 24 24">
                <path fill="currentColor" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4Z"/>
              </svg>
              <span v-if="!sidebarCollapsed">Países</span>
            </router-link>
          </li>
          <li>
            <router-link to="/keywords" class="nav-item">
              <svg class="nav-icon" viewBox="0 0 24 24">
                <path fill="currentColor" d="M5.5,7A1.5,1.5 0 0,1 4,5.5A1.5,1.5 0 0,1 5.5,4A1.5,1.5 0 0,1 7,5.5A1.5,1.5 0 0,1 5.5,7M21.41,11.58L12.41,2.58C12.05,2.22 11.55,2 11,2H4C2.89,2 2,2.89 2,4V11C2,11.55 2.22,12.05 2.59,12.41L11.58,21.41C11.95,21.77 12.45,22 13,22C13.55,22 14.05,21.77 14.41,21.41L21.41,14.41C21.77,14.05 22,13.55 22,13C22,12.45 21.77,11.95 21.41,11.58Z"/>
              </svg>
              <span v-if="!sidebarCollapsed">Palabras Clave</span>
            </router-link>
          </li>
          <li>
            <router-link to="/publication-types" class="nav-item">
              <svg class="nav-icon" viewBox="0 0 24 24">
                <path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
              </svg>
              <span v-if="!sidebarCollapsed">Tipos de Publicación</span>
            </router-link>
          </li>
        </ul>
      </div>

      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">
            {{ userInitials }}
          </div>
          <div v-if="!sidebarCollapsed" class="user-details">
            <p class="user-name">{{ user?.first_name }} {{ user?.last_name }}</p>
            <p class="user-role">{{ user?.role }}</p>
          </div>
        </div>
        <button @click="handleLogout" class="logout-btn" :title="sidebarCollapsed ? 'Cerrar Sesión' : ''">
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path fill="currentColor" d="M16,17V14H9V10H16V7L21,12L16,17M14,2A2,2 0 0,1 16,4V6H14V4H5V20H14V18H16V20A2,2 0 0,1 14,22H5A2,2 0 0,1 3,20V4A2,2 0 0,1 5,2H14Z"/>
          </svg>
          <span v-if="!sidebarCollapsed">Cerrar Sesión</span>
        </button>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content" :class="{ 'main-expanded': sidebarCollapsed }">
      <header class="main-header">
        <div class="header-content">
          <h1 class="page-title">{{ pageTitle }}</h1>
          <div class="header-actions">
            <button class="notification-btn">
              <svg viewBox="0 0 24 24" width="20" height="20">
                <path fill="currentColor" d="M10,21H14A2,2 0 0,1 12,23A2,2 0 0,1 10,21M21,19V20H3V19L5,17V11C5,7.9 7.03,5.17 10,4.29C10,4.19 10,4.1 10,4A2,2 0 0,1 12,2A2,2 0 0,1 14,4C14,4.1 14,4.19 14,4.29C16.97,5.17 19,7.9 19,11V17L21,19M17,11A5,5 0 0,0 12,6A5,5 0 0,0 7,11V18H17V11Z"/>
              </svg>
            </button>
          </div>
        </div>
      </header>

      <div class="content-area">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const sidebarCollapsed = ref(false)

const user = computed(() => authStore.user)
const userInitials = computed(() => {
  if (!user.value) return 'U'
  const first = user.value.first_name?.[0] || ''
  const last = user.value.last_name?.[0] || ''
  return (first + last).toUpperCase() || 'U'
})

const pageTitle = computed(() => {
  const titles = {
    dashboard: 'Dashboard',
    countries: 'Gestión de Países',
    keywords: 'Gestión de Palabras Clave',
    'publication-types': 'Tipos de Publicación'
  }
  return titles[route.name] || 'Academic Management'
})

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const handleLogout = async () => {
  if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
    await authStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  background-color: #f8fafc;
}

.sidebar {
  width: 280px;
  background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.sidebar-collapsed {
  width: 80px;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #e2e8f0;
}

.toggle-btn {
  background: none;
  border: none;
  color: #e2e8f0;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.toggle-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.sidebar-content {
  flex: 1;
  padding: 20px 0;
}

.nav-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-menu li {
  margin-bottom: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: #cbd5e0;
  text-decoration: none;
  transition: all 0.2s;
  border-radius: 0;
  position: relative;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.router-link-active {
  background-color: rgba(102, 126, 234, 0.2);
  color: white;
  border-right: 4px solid #667eea;
}

.nav-icon {
  width: 20px;
  height: 20px;
  margin-right: 12px;
  flex-shrink: 0;
}

.sidebar-collapsed .nav-icon {
  margin-right: 0;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  margin-right: 12px;
  flex-shrink: 0;
}

.sidebar-collapsed .user-avatar {
  margin-right: 0;
}

.user-details {
  min-width: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  margin: 0 0 4px 0;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 12px;
  color: #a0aec0;
  margin: 0;
  text-transform: capitalize;
}

.logout-btn {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 10px;
  background: rgba(220, 38, 38, 0.1);
  border: 1px solid rgba(220, 38, 38, 0.3);
  color: #fca5a5;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
}

.logout-btn:hover {
  background: rgba(220, 38, 38, 0.2);
  color: #f87171;
}

.logout-btn svg {
  margin-right: 8px;
  flex-shrink: 0;
}

.sidebar-collapsed .logout-btn svg {
  margin-right: 0;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: margin-left 0.3s ease;
}

.main-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 0 30px;
  height: 70px;
  display: flex;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #2d3748;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.notification-btn {
  background: none;
  border: none;
  color: #718096;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s;
}

.notification-btn:hover {
  background-color: #f7fafc;
  color: #2d3748;
}

.content-area {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
  background-color: #f8fafc;
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: -280px;
    top: 0;
    bottom: 0;
    z-index: 1000;
  }
  
  .sidebar.sidebar-open {
    left: 0;
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .content-area {
    padding: 20px;
  }
}
</style>