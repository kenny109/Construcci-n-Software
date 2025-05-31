<!-- src/components/layout/AppLayout.vue -->
<template>
  <div class="app-layout">
    <!-- Header -->
    <AppHeader />
    
    <!-- Main Container -->
    <div class="main-container">
      <!-- Sidebar -->
      <AppSidebar />
      
      <!-- Main Content Area -->
      <main class="main-content">
        <div class="content-wrapper">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'

const authStore = useAuthStore()

onMounted(() => {
  // Inicializar autenticación si no está inicializada
  if (!authStore.user && localStorage.getItem('access_token')) {
    authStore.initializeAuth()
  }
})
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.main-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: #ffffff;
  border-radius: 8px 0 0 0;
  box-shadow: -2px 0 4px rgba(0, 0, 0, 0.1);
}

.content-wrapper {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* Responsive design */
@media (max-width: 768px) {
  .main-container {
    flex-direction: column;
  }
  
  .content-wrapper {
    padding: 16px;
  }
}
</style>