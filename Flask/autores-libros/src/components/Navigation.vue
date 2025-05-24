<template>
  <nav class="navigation">
    <div class="nav-header">
      <h2 class="nav-title">Biblioteca</h2>
      <p class="nav-subtitle">Sistema de Gestión</p>
    </div>
    
    <div class="nav-menu">
      <router-link 
        to="/autores" 
        class="nav-item"
        :class="{ active: $route.path === '/autores' }"
      >
        📚 Autores
      </router-link>
      
      <router-link 
        to="/libros" 
        class="nav-item"
        :class="{ active: $route.path === '/libros' }"
      >
        📖 Libros
      </router-link>
      
      <router-link 
        to="/generos" 
        class="nav-item"
        :class="{ active: $route.path === '/generos' }"
      >
        🏷️ Géneros
      </router-link>
    </div>
    
    <div class="nav-footer">
      <button @click="logout" class="btn btn-danger btn-sm" style="width: 100%;">
        🚪 Cerrar Sesión
      </button>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navigation',
  methods: {
    logout() {
      if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
        localStorage.removeItem('token')
        this.$router.push('/login')
      }
    }
  }
}
</script>