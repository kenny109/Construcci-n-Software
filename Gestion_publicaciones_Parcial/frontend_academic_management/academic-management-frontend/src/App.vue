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
            👤 {{ currentUser?.first_name}}
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

        <!-- Configuración -->
        <div v-if="activeTab === 'config'" class="config-section">
          <h2>⚙️ Configuración</h2>
          <div class="config-grid">
            <div class="config-card">
              <h3>🌍 Países</h3>
              <p>Gestionar países disponibles</p>
              <button @click="showConfigModal = 'countries'" class="config-btn">
                Configurar
              </button>
            </div>
            <div class="config-card">
              <h3>🏷️ Palabras Clave</h3>
              <p>Gestionar palabras clave</p>
              <button @click="showConfigModal = 'keywords'" class="config-btn">
                Configurar
              </button>
            </div>
            <div class="config-card">
              <h3>📑 Tipos de Publicación</h3>
              <p>Gestionar tipos de publicación</p>
              <button @click="showConfigModal = 'publication-types'" class="config-btn">
                Configurar
              </button>
            </div>
          </div>
        </div>
      </main>

      <!-- Modal de configuración -->
      <div v-if="showConfigModal" class="modal-overlay" @click="closeConfigModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Configurar {{ getConfigTitle(showConfigModal) }}</h3>
            <button @click="closeConfigModal" class="close-btn">✕</button>
          </div>
          <div class="modal-body">
            <!-- Países -->
            <CountriesTable 
              v-if="showConfigModal === 'countries'"
              :items="configData.countries"
              :loading="configLoading"
              :currentPage="configPagination.currentPage"
              :totalPages="configPagination.totalPages"
              @create="handleConfigCreate('countries')"
              @edit="handleConfigEdit('countries', $event)"
              @delete="handleConfigDelete('countries', $event)"
              @search="handleConfigSearch('countries', $event)"
              @page-change="handleConfigPageChange($event)"
            />
            
            <!-- Palabras Clave -->
            <KeywordsTable 
              v-if="showConfigModal === 'keywords'"
              :items="configData.keywords"
              :loading="configLoading"
              :currentPage="configPagination.currentPage"
              :totalPages="configPagination.totalPages"
              @create="handleConfigCreate('keywords')"
              @edit="handleConfigEdit('keywords', $event)"
              @delete="handleConfigDelete('keywords', $event)"
              @search="handleConfigSearch('keywords', $event)"
              @page-change="handleConfigPageChange($event)"
            />
            
            <!-- Tipos de Publicación -->
            <PublicationTypesTable 
              v-if="showConfigModal === 'publication-types'"
              :items="configData.publicationTypes"
              :loading="configLoading"
              :currentPage="configPagination.currentPage"
              :totalPages="configPagination.totalPages"
              @create="handleConfigCreate('publication-types')"
              @edit="handleConfigEdit('publication-types', $event)"
              @delete="handleConfigDelete('publication-types', $event)"
              @search="handleConfigSearch('publication-types', $event)"
              @page-change="handleConfigPageChange($event)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LoginComponent from './components/LoginComponent.vue'
import PublicationsComponent from './components/PublicationCrud.vue'
import CountriesTable from './components/CountriesTable.vue'
import KeywordsTable from './components/KeywordsTable.vue'
import PublicationTypesTable from './components/PublicationTypesTable.vue'
import api from './services/api'

export default {
  name: 'App',
  components: {
    LoginComponent,
    PublicationsComponent,
    CountriesTable,
    KeywordsTable,
    PublicationTypesTable
  },
  data() {
    return {
      isAuthenticated: false,
      currentUser: null,
      activeTab: 'publications',
      showConfigModal: null,
      configLoading: false,
      stats: {
        publications: 0,
        authors: 0,
        keywords: 0,
        countries: 0
      },
      recentActivity: [],
      configData: {
        countries: [],
        keywords: [],
        publicationTypes: []
      },
      configPagination: {
        currentPage: 1,
        totalPages: 1
      },
      tabs: [
        { id: 'dashboard', name: 'Dashboard', icon: '📊' },
        { id: 'publications', name: 'Publicaciones', icon: '📄' },
        { id: 'config', name: 'Configuración', icon: '⚙️' }
      ]
    }
  },
  computed: {
    availableTabs() {
      if (this.currentUser?.role === 'admin') {
        return this.tabs
      } else {
        return this.tabs.filter(tab => tab.id !== 'dashboard')
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
        const [publications, countries, keywords, publicationTypes] = await Promise.all([
          api.getItems('publications').catch(() => ({ data: [] })),
          api.getCountries().catch(() => ({ data: [] })),
          api.getKeywords().catch(() => ({ data: [] })),
          api.getPublicationTypes().catch(() => ({ data: [] }))
        ])
        
        this.stats = {
          publications: publications.data?.length || 0,
          countries: countries.data?.length || 0,
          keywords: keywords.data?.length || 0,
          publicationTypes: publicationTypes.data?.length || 0
        }
      } catch (error) {
        console.error('Error cargando estadísticas:', error)
      }
    },
    
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
    
    async loadConfigData(type) {
      this.configLoading = true
      try {
        let response
        switch (type) {
          case 'countries':
            response = await api.getCountries()
            this.configData.countries = response.data || []
            break
          case 'keywords':
            response = await api.getKeywords()
            this.configData.keywords = response.data || []
            break
          case 'publication-types':
            response = await api.getPublicationTypes()
            this.configData.publicationTypes = response.data || []
            break
        }
      } catch (error) {
        console.error(`Error cargando ${type}:`, error)
      } finally {
        this.configLoading = false
      }
    },
    
    getConfigTitle(modalType) {
      const titles = {
        'countries': 'Países',
        'keywords': 'Palabras Clave',
        'publication-types': 'Tipos de Publicación'
      }
      return titles[modalType] || 'Configuración'
    },
    
    async closeConfigModal() {
      this.showConfigModal = null
      this.configPagination.currentPage = 1
    },
    
    async handleConfigCreate(type) {
      console.log(`Crear nuevo ${type}`)
      // Aquí implementarías la lógica de creación
    },
    
    async handleConfigEdit(type, item) {
      console.log(`Editar ${type}:`, item)
      // Aquí implementarías la lógica de edición
    },
    
    async handleConfigDelete(type, id) {
      if (confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
        try {
          switch (type) {
            case 'countries':
              await api.deleteCountry(id)
              break
            case 'keywords':
              await api.deleteKeyword(id)
              break
            case 'publication-types':
              await api.deletePublicationType(id)
              break
          }
          await this.loadConfigData(type)
        } catch (error) {
          console.error(`Error eliminando ${type}:`, error)
          alert('Error al eliminar el elemento')
        }
      }
    },
    
    async handleConfigSearch(type, searchTerm) {
      console.log(`Buscar en ${type}:`, searchTerm)
      // Aquí implementarías la lógica de búsqueda
      await this.loadConfigData(type)
    },
    
    async handleConfigPageChange(page) {
      this.configPagination.currentPage = page
      await this.loadConfigData(this.showConfigModal)
    },
    
    formatDate(date) {
      return new Date(date).toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    }
  },
  
  watch: {
    showConfigModal(newValue) {
      if (newValue) {
        this.loadConfigData(newValue)
      }
    }
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

/* Config Section */
.config-section h2 {
  color: white;
  margin-bottom: 2rem;
  font-size: 2rem;
  text-align: center;
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.config-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s ease;
}

.config-card:hover {
  transform: translateY(-5px);
}

.config-card h3 {
  color: #4a5568;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.config-card p {
  color: #718096;
  margin-bottom: 1.5rem;
}

.config-btn {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea, #252e64);
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.config-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 15px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #667eea, #252e64);
  color: white;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.3rem;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: background 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.modal-body {
  padding: 2rem;
  max-height: 70vh;
  overflow-y: auto;
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