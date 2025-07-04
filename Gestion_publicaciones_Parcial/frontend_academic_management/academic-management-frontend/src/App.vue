<template>
  <div id="app">
    <!-- Componente de Login si no está autenticado -->
    <LoginComponent 
      v-if="!isAuthenticated" 
      @login-success="handleLoginSuccess"
    />
    
    <!-- Aplicación principal si está autenticado -->
    <div v-else class="app-container">
      <!-- Barra de navegación -->
      <nav class="navbar">
        <div class="nav-brand">
          <h1>📚 Gestión Académica</h1>
        </div>
        
        <div class="nav-menu">
          <button 
            v-for="tab in availableTabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="['nav-btn', { active: activeTab === tab.id }]"
          >
            {{ tab.icon }} {{ tab.name }}
          </button>
        </div>
        
        <div class="nav-user">
          <span class="user-info">
            👤 {{ currentUser?.first_name || 'Usuario'}}
          </span>
          <button @click="handleLogout" class="logout-btn">
            🚪 Cerrar Sesión
          </button>
        </div>
      </nav>

      <!-- Contenido principal -->
      <main class="main-content">
        <!-- Dashboard -->
        <div v-if="activeTab === 'dashboard'" class="dashboard">
          <h2>📊 Dashboard</h2>
          <div class="stats-grid">
            <div class="stat-card">
              <h3>📄 Publicaciones</h3>
              <p class="stat-number">{{ stats.publications || 0 }}</p>
            </div>
            <div class="stat-card">
              <h3>👥 Autores</h3>
              <p class="stat-number">{{ stats.authors || 0 }}</p>
            </div>
            <div class="stat-card">
              <h3>🏷️ Palabras Clave</h3>
              <p class="stat-number">{{ stats.keywords || 0 }}</p>
            </div>
            <div class="stat-card">
              <h3>🌍 Países</h3>
              <p class="stat-number">{{ stats.countries || 0 }}</p>
            </div>
          </div>
          
          <div class="recent-activity">
            <h3>📈 Actividad Reciente</h3>
            <div class="activity-list">
              <p v-if="!recentActivity.length" class="no-data">
                No hay actividad reciente
              </p>
              <div 
                v-for="activity in recentActivity" 
                :key="activity.id"
                class="activity-item"
              >
                <span class="activity-icon">{{ activity.icon }}</span>
                <span class="activity-text">{{ activity.text }}</span>
                <span class="activity-time">{{ formatDate(activity.date) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Publicaciones -->
        <PublicationsComponent 
          v-if="activeTab === 'publications'" 
          @update-stats="loadStats"
        />
        <!-- ORCID -->
<OrcidComponent 
  v-if="activeTab === 'orcid'"
  :current-user="currentUser"
  @researcher-synced="handleResearcherSynced"
  @publications-added="handlePublicationsAdded"
/>
      <!-- Configuración -->
      <ConfigComponent 
        v-if="activeTab === 'config'" 
        @show-success="handleShowSuccess"
        @show-error="handleShowError"
      />
      </main>

    </div>
  </div>
</template>

<script>
import LoginComponent from './components/LoginComponent.vue'
import PublicationsComponent from './components/PublicationCrud.vue'
import ConfigComponent from './components/ConfigComponent.vue'
import OrcidComponent from './components/OrcidComponent.vue'
import api from './services/api'

export default {
  name: 'App',
  components: {
    LoginComponent,
    PublicationsComponent,
    ConfigComponent,
    OrcidComponent
  },
  data() {
    return {
      isAuthenticated: false,
      currentUser: null,
      activeTab: 'publications',
      publicationsCount: 0,
      stats: {
        publications: 0,
        authors: 0,
        keywords: 0,
        countries: 0
      },
      recentActivity: [],
      tabs: [
        { id: 'dashboard', name: 'Dashboard', icon: '📊' },
        { id: 'publications', name: 'Publicaciones', icon: '📄' },
         { id: 'orcid', name: 'ORCID', icon: '🔬' },
        { id: 'config', name: 'Configuración', icon: '⚙️' }
      ],
      
    }
  },
  computed: {
  availableTabs() {
    if (this.currentUser?.role === 'admin') {
      return this.tabs
    } else {
      // Los usuarios normales pueden ver publicaciones y ORCID
      return this.tabs.filter(tab => !['dashboard', 'config'].includes(tab.id))
    }
  }
},
  async mounted() {
    this.checkAuthentication()
    if (this.isAuthenticated) {
      if (this.currentUser?.role === 'admin') {
        await this.loadStats()
        await this.loadRecentActivity()
      } else {
        this.activeTab = 'publications'
      }
    }
  },
  methods: {
    checkAuthentication() {
      const token = localStorage.getItem('token')
      const user = localStorage.getItem('user')
      
      if (token && user) {
        this.isAuthenticated = true
        this.currentUser = JSON.parse(user)
      }
    },
    
    handleLoginSuccess(userData) {
      this.isAuthenticated = true
      this.currentUser = userData.user
      if (userData.user?.role === 'admin') {
        this.loadStats()
        this.loadRecentActivity()
      } else {
        this.activeTab = 'publications'
      }
    },
    
    async handleLogout() {
      try {
        api.logout()
        this.isAuthenticated = false
        this.currentUser = null
        this.activeTab = 'publications'
      } catch (error) {
        console.error('Error al cerrar sesión:', error)
      }
    },
    
    async loadStats() {
  try {
    const [
      publicationsCount,
      authors,
      keywords,
      countries,
      publicationTypes
    ] = await Promise.all([
      api.getPublicationsCount().catch(() => ({ total: 0 })),
      api.getItems('authors').catch(() => ({ data: [] })),
      api.getKeywords().catch(() => ({ data: [] })),
      api.getCountries().catch(() => ({ data: [] })),
      api.getPublicationTypes().catch(() => ({ data: [] }))
    ]);

    this.stats = {
      publications: publicationsCount.total || 0,
      authors: authors.data?.length || 0,
      keywords: keywords.data?.length || 0,
      countries: countries.data?.length || 0,
      publicationTypes: publicationTypes.data?.length || 0
    };
  } catch (error) {
    console.error('Error cargando estadísticas:', error);
  }
}


,
    
    async loadRecentActivity() {
      try {
        this.recentActivity = [
          {
            id: 1,
            icon: '📄',
            text: 'Nueva publicación agregada',
            date: new Date()
          },
          {
            id: 2,
            icon: '👤',
            text: 'Nuevo autor registrado',
            date: new Date(Date.now() - 86400000)
          }
        ]
      } catch (error) {
        console.error('Error cargando actividad:', error)
      }
    },    
    formatDate(date) {
      return new Date(date).toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    }
  },
  
 handleResearcherSynced(researcher) {
  console.log('Investigador sincronizado:', researcher)
  // Aquí puedes manejar la sincronización del investigador
  // Por ejemplo, recargar estadísticas si es admin
  if (this.currentUser?.role === 'admin') {
    this.loadStats()
  }
},

handlePublicationsAdded(count) {
  console.log(`${count} publicaciones añadidas desde ORCID`)
  // Recargar estadísticas si es admin
  if (this.currentUser?.role === 'admin') {
    this.loadStats()
  }
  // Mostrar mensaje de éxito
  this.showMessage(`${count} publicaciones añadidas exitosamente desde ORCID`, 'success')
},

showMessage(text, type = 'info') {
  // Puedes implementar un sistema de notificaciones aquí
  console.log(`${type.toUpperCase()}: ${text}`)
}
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  background: linear-gradient(135deg, #969597 0%, #f8f9fa 100%);
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Navbar */
.navbar {
  background: rgba(252, 251, 251, 0.95);
  backdrop-filter: blur(10px);
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-brand h1 {
  color: #2c3e50;
  font-size: 1.5rem;
  font-weight: 700;
}

.nav-menu {
  display: flex;
  gap: 0.5rem;
}

.nav-btn {
  padding: 0.75rem 1.5rem;
  background: transparent;
  border: 2px solid transparent;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  color: #6c757d;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background: rgba(102, 126, 234, 0.1);
  border-color: rgba(34, 47, 105, 0.3);
}

.nav-btn.active {
  background: linear-gradient(135deg, #263781, #363a4e);
  color: white;
  border-color: transparent;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  color: #4a5568;
  font-weight: 500;
}

.logout-btn {
  padding: 0.5rem 1rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: #c53030;
  transform: translateY(-1px);
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

/* Dashboard */
.dashboard h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 2rem;
  text-align: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card h3 {
  color: #4a5568;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.stat-number {
  font-size: 3rem;
  font-weight: bold;
  color: #323e75;
  margin: 0;
}

/* Recent Activity */
.recent-activity {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.recent-activity h3 {
  color: #4a5568;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 10px;
  border-left: 4px solid #243270bb;
}

.activity-icon {
  font-size: 1.2rem;
}

.activity-text {
  flex: 1;
  color: #4a5568;
}

.activity-time {
  color: #718096;
  font-size: 0.9rem;
}

.no-data {
  text-align: center;
  color: #718096;
  font-style: italic;
  padding: 2rem;
}




/* Responsive */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .nav-menu {
    flex-wrap: wrap;
    justify-content: center;
  }

  .main-content {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .nav-btn {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
}
</style>