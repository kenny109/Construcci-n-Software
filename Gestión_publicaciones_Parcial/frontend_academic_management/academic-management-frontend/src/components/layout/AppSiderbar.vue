<!-- src/components/layout/AppSidebar.vue -->
<template>
  <aside class="sidebar" :class="{ 'sidebar--collapsed': isCollapsed }">
    <div class="sidebar__header">
      <div class="sidebar__logo">
        <img src="@/assets/logo.svg" alt="Logo" class="sidebar__logo-img" />
        <span v-if="!isCollapsed" class="sidebar__logo-text">Academic Mgmt</span>
      </div>
      <button 
        class="sidebar__toggle"
        @click="toggleSidebar"
        :aria-label="isCollapsed ? 'Expandir menú' : 'Contraer menú'"
      >
        <span class="sidebar__toggle-icon"></span>
      </button>
    </div>

    <nav class="sidebar__nav">
      <ul class="sidebar__menu">
        <li class="sidebar__menu-item">
          <RouterLink to="/dashboard" class="sidebar__menu-link">
            <span class="sidebar__menu-icon">📊</span>
            <span v-if="!isCollapsed" class="sidebar__menu-text">Dashboard</span>
          </RouterLink>
        </li>
        
        <li class="sidebar__menu-section">
          <span v-if="!isCollapsed" class="sidebar__menu-section-title">Maestros</span>
        </li>
        
        <li class="sidebar__menu-item">
          <RouterLink to="/countries" class="sidebar__menu-link">
            <span class="sidebar__menu-icon">🌍</span>
            <span v-if="!isCollapsed" class="sidebar__menu-text">Países</span>
          </RouterLink>
        </li>
        
        <li class="sidebar__menu-item">
          <RouterLink to="/keywords" class="sidebar__menu-link">
            <span class="sidebar__menu-icon">🏷️</span>
            <span v-if="!isCollapsed" class="sidebar__menu-text">Palabras Clave</span>
          </RouterLink>
        </li>
        
        <li class="sidebar__menu-item">
          <RouterLink to="/publication-types" class="sidebar__menu-link">
            <span class="sidebar__menu-icon">📚</span>
            <span v-if="!isCollapsed" class="sidebar__menu-text">Tipos de Publicación</span>
          </RouterLink>
        </li>
        
        <li class="sidebar__menu-section">
          <span v-if="!isCollapsed" class="sidebar__menu-section-title">Gestión</span>
        </li>
        
        <li class="sidebar__menu-item">
          <RouterLink to="/authors" class="sidebar__menu-link">
            <span class="sidebar__menu-icon">👥</span>
            <span v-if="!isCollapsed" class="sidebar__menu-text">Autores</span>
          </RouterLink>
        </li>
        
        <li class="sidebar__menu-item">
          <RouterLink to="/publications" class="sidebar__menu-link">
            <span class="sidebar__menu-icon">📄</span>
            <span v-if="!isCollapsed" class="sidebar__menu-text">Publicaciones</span>
          </RouterLink>
        </li>
        
        <li class="sidebar__menu-item">
          <RouterLink to="/projects" class="sidebar__menu-link">
            <span class="sidebar__menu-icon">🚀</span>
            <span v-if="!isCollapsed" class="sidebar__menu-text">Proyectos</span>
          </RouterLink>
        </li>
      </ul>
    </nav>

    <div class="sidebar__footer">
      <div class="sidebar__user" v-if="user">
        <div class="sidebar__user-avatar">
          {{ userInitials }}
        </div>
        <div v-if="!isCollapsed" class="sidebar__user-info">
          <span class="sidebar__user-name">{{ user.first_name }} {{ user.last_name }}</span>
          <span class="sidebar__user-role">{{ user.role }}</span>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const isCollapsed = ref(false)

const user = computed(() => authStore.user)
const userInitials = computed(() => {
  if (!user.value) return 'U'
  const first = user.value.first_name?.[0] || ''
  const last = user.value.last_name?.[0] || ''
  return (first + last).toUpperCase() || user.value.username?.[0]?.toUpperCase() || 'U'
})

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}
</script>

<style scoped>
.sidebar {
  width: 280px;
  height: 100vh;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
}

.sidebar--collapsed {
  width: 70px;
}

.sidebar__header {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 64px;
}

.sidebar__logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sidebar__logo-img {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
}

.sidebar__logo-text {
  font-weight: 600;
  font-size: 1.125rem;
  color: #1f2937;
  white-space: nowrap;
  overflow: hidden;
}

.sidebar__toggle {
  background: none;
  border: none;
  padding: 0.5rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.sidebar__toggle:hover {
  background-color: #f3f4f6;
}

.sidebar__toggle-icon {
  display: block;
  width: 20px;
  height: 2px;
  background: #6b7280;
  position: relative;
}

.sidebar__toggle-icon::before,
.sidebar__toggle-icon::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 2px;
  background: #6b7280;
  transition: transform 0.3s ease;
}

.sidebar__toggle-icon::before {
  top: -6px;
}

.sidebar__toggle-icon::after {
  top: 6px;
}

.sidebar__nav {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 0;
}

.sidebar__menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar__menu-section {
  padding: 0.75rem 1rem 0.5rem;
}

.sidebar__menu-section-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.sidebar__menu-item {
  margin: 0.25rem 0;
}

.sidebar__menu-link {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: #4b5563;
  text-decoration: none;
  border-radius: 0.375rem;
  margin: 0 0.5rem;
  transition: all 0.2s ease;
  gap: 0.75rem;
}

.sidebar__menu-link:hover {
  background-color: #f3f4f6;
  color: #1f2937;
}

.sidebar__menu-link.router-link-active {
  background-color: #3b82f6;
  color: white;
}

.sidebar__menu-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
  width: 20px;
  text-align: center;
}

.sidebar__menu-text {
  white-space: nowrap;
  overflow: hidden;
}

.sidebar__footer {
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
}

.sidebar__user {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.sidebar__user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #3b82f6;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.sidebar__user-info {
  min-width: 0;
  flex: 1;
}

.sidebar__user-name {
  display: block;
  font-weight: 500;
  color: #1f2937;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.875rem;
}

.sidebar__user-role {
  display: block;
  font-size: 0.75rem;
  color: #6b7280;
  text-transform: capitalize;
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .sidebar--open {
    transform: translateX(0);
  }
}
</style>