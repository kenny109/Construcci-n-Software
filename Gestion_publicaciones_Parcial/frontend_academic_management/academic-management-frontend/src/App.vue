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
.app-container {
  min-height: 100vh;
  background: #f8f9fa;
}

.navbar {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand h1 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.5rem;
}

.nav-menu {
  display: flex;
  gap: 1rem;
}

.nav-btn {
  background: transparent;
  border: 2px solid transparent;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #6c757d;
}

.nav-btn:hover {
  background: #e9ecef;
  color: #495057;
}

.nav-btn.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  color: #6c757d;
  font-weight: 500;
}

.logout-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.logout-btn:hover {
  background: #c82333;
}

.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  text-align: center;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card h3 {
  margin: 0 0 1rem 0;
  color: #6c757d;
  font-size: 1rem;
}

.stat-number {
  font-size: 3rem;
  font-weight: bold;
  color: #007bff;
  margin: 0;
}

.recent-activity {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.recent-activity h3 {
  margin-top: 0;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.activity-list {
  max-height: 300px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #e9ecef;
  gap: 1rem;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  font-size: 1.2rem;
}

.activity-text {
  flex: 1;
  color: #495057;
}

.activity-time {
  color: #6c757d;
  font-size: 0.9rem;
}

.no-data {
  text-align: center;
  color: #6c757d;
  font-style: italic;
  padding: 2rem;
}

.config-section h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.config-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  text-align: center;
  transition: transform 0.3s ease;
}

.config-card:hover {
  transform: translateY(-5px);
}

.config-card h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1.5rem;
}

.config-card p {
  color: #6c757d;
  margin-bottom: 2rem;
  line-height: 1.5;
}

.config-btn {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s ease;
}

.config-btn:hover {
  background: #0056b3;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 25px rgba(0,0,0,0.1);
  width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e9ecef;
  background: #f8f9fa;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background 0.3s ease;
}

.close-btn:hover {
  background: #e9ecef;
  color: #495057;
}

.modal-body {
  padding: 2rem;
  max-height: 70vh;
  overflow-y: auto;
}
</style>