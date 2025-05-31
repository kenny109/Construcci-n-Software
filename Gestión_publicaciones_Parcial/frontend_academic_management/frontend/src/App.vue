<template>
  <div id="app">
    <header class="header" v-if="!isLoginPage">
      <nav class="nav">
        <div class="nav-brand">
          <h1>Sistema de Gestión de Publicaciones</h1>
        </div>
        <div class="nav-menu">
          <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
          <router-link to="/authors" class="nav-link">Autores</router-link>
          <router-link to="/publications" class="nav-link">Publicaciones</router-link>
          <button @click="logout" class="btn-logout">Cerrar Sesión</button>
        </div>
      </nav>
    </header>
    
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

export default {
  name: 'App',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    
    const isLoginPage = computed(() => route.name === 'Login')
    
    const logout = async () => {
      await authStore.logout()
      router.push('/login')
    }
    
    return {
      isLoginPage,
      logout
    }
  }
}
</script>
