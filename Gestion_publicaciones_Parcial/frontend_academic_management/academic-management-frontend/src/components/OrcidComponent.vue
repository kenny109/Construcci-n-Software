<template>
  <div class="orcid-container">
    <div class="orcid-header">
      <h2>🔬 Integración ORCID</h2>
      <p class="orcid-description">
        Busca y sincroniza información de investigadores desde ORCID
      </p>
    </div>

    <!-- Buscador de investigador -->
    <div class="search-section">
      <div class="search-form">
        <div class="input-group">
          <input
            v-model="orcidId"
            type="text"
            placeholder="Ingresa ORCID ID (ej: 0000-0000-0000-0000)"
            class="orcid-input"
            @keyup.enter="searchResearcher"
          />
          <button 
            @click="searchResearcher"
            :disabled="loading || !orcidId"
            class="search-btn"
          >
            <span v-if="loading">⏳</span>
            <span v-else>🔍</span>
            {{ loading ? 'Buscando...' : 'Buscar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Información del investigador -->
    <div v-if="researcher" class="researcher-info">
      <div class="researcher-card">
        <div class="researcher-header">
          <h3>👤 {{ researcher.credit_name || `${researcher.first_name} ${researcher.last_name}` }}</h3>
          <div class="researcher-meta">
            <span class="orcid-badge">🆔 {{ researcher.orcid_id }}</span>
            <span v-if="researcher.email" class="email">📧 {{ researcher.email }}</span>
          </div>
          <p v-if="researcher.affiliation" class="affiliation">
            🏢 {{ researcher.affiliation }}
          </p>
        </div>
        
        <div class="researcher-actions">
          <button 
            @click="loadWorks"
            :disabled="loadingWorks"
            class="action-btn load-works"
          >
            <span v-if="loadingWorks">⏳</span>
            <span v-else>📚</span>
            {{ loadingWorks ? 'Cargando...' : 'Cargar Publicaciones' }}
          </button>
          
          <button 
            @click="syncResearcher"
            :disabled="syncing"
            class="action-btn sync-btn"
          >
            <span v-if="syncing">🔄</span>
            <span v-else>🔄</span>
            {{ syncing ? 'Sincronizando...' : 'Sincronizar Todo' }}
          </button>
          <button 
  @click="addAuthorFromOrcid"
  :disabled="syncing"
  class="action-btn add-author-btn"
>
  <span v-if="syncing">👤⏳</span>
  <span v-else>👤➕</span>
  {{ syncing ? 'Añadiendo...' : 'Añadir como Autor' }}
</button>

        </div>
      </div>
    </div>

    <!-- Lista de publicaciones -->
    <div v-if="works.length > 0" class="works-section">
      <div class="works-header">
        <h3>📚 Publicaciones encontradas ({{ works.length }})</h3>
        <div class="works-actions">
          <button 
            @click="selectAll"
            class="action-btn select-all"
          >
            {{ allSelected ? '❌ Deseleccionar Todo' : '✅ Seleccionar Todo' }}
          </button>
          <button 
            @click="addSelectedWorks"
            :disabled="selectedWorks.length === 0 || adding"
            class="action-btn add-selected"
          >
            <span v-if="adding">⏳</span>
            <span v-else>➕</span>
            {{ adding ? 'Añadiendo...' : `Añadir Seleccionadas (${selectedWorks.length})` }}
          </button>
          <button 
            @click="addSelectedWorksBatch"
            :disabled="selectedWorks.length === 0 || addingBatch"
            class="action-btn add-batch"
          >
            <span v-if="addingBatch">⏳</span>
            <span v-else>📦</span>
            {{ addingBatch ? 'Añadiendo en lote...' : `Lote (${selectedWorks.length})` }}
          </button>
        </div>
      </div>

      <div class="works-grid">
        <div 
          v-for="work in works" 
          :key="work.external_id || work.title"
          class="work-card"
          :class="{ selected: selectedWorks.includes(work) }"
        >
          <div class="work-header">
            <input
              type="checkbox"
              :checked="selectedWorks.includes(work)"
              @change="toggleWorkSelection(work)"
              class="work-checkbox"
            />
            <h4 class="work-title">{{ work.title }}</h4>
          </div>
          
          <div class="work-meta">
            <span v-if="work.type" class="work-type">📄 {{ work.type }}</span>
            <span v-if="work.year" class="work-year">📅 {{ work.year }}</span>
          </div>
          
          <div class="work-details">
            <p v-if="work.journal" class="work-journal">
              📖 <strong>Revista:</strong> {{ work.journal }}
            </p>
            <p v-if="work.doi" class="work-doi">
              🔗 <strong>DOI:</strong> 
              <a :href="`https://doi.org/${work.doi}`" target="_blank">{{ work.doi }}</a>
            </p>
            <p v-if="work.url" class="work-url">
              🌐 <strong>URL:</strong> 
              <a :href="work.url" target="_blank">{{ work.url }}</a>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Mensajes -->
    <div v-if="message" class="message" :class="messageType">
      {{ message }}
    </div>

    <!-- Logs de operaciones -->
    <div v-if="operationLogs.length > 0" class="logs-section">
      <h4>📋 Logs de Operaciones</h4>
      <div class="logs-container">
        <div 
          v-for="(log, index) in operationLogs" 
          :key="index"
          class="log-item"
          :class="log.type"
        >
          <span class="log-timestamp">{{ formatTime(log.timestamp) }}</span>
          <span class="log-message">{{ log.message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'OrcidComponent',
  props: {
    currentUser: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      orcidId: '',
      researcher: null,
      works: [],
      selectedWorks: [],
      loading: false,
      loadingWorks: false,
      syncing: false,
      adding: false,
      addingBatch: false,
      message: '',
      messageType: 'info',
      operationLogs: []
    }
  },
  computed: {
    allSelected() {
      return this.works.length > 0 && this.selectedWorks.length === this.works.length
    },
    isAdmin() {
      return this.currentUser?.role === 'admin'
    }
  },
  methods: {
    async searchResearcher() {
      if (!this.orcidId.trim()) {
        this.showMessage('Por favor ingresa un ORCID ID válido', 'error')
        return
      }

      this.loading = true
      this.researcher = null
      this.works = []
      this.selectedWorks = []
      this.clearLogs()

      try {
        this.addLog('Buscando información del investigador...', 'info')
        
        // Usar el método correcto de la API
        const response = await api.getOrcidResearcher(this.orcidId)

        if (response.success) {
          this.researcher = response.data
          this.showMessage('Información del investigador cargada exitosamente', 'success')
          this.addLog('Información del investigador obtenida correctamente', 'success')
        } else {
          this.showMessage(response.message || 'No se pudo obtener la información del investigador', 'error')
          this.addLog('Error al obtener información del investigador', 'error')
        }
      } catch (error) {
        console.error('Error al buscar investigador:', error)
        this.showMessage(error.message || 'Error al buscar el investigador. Verifica el ORCID ID.', 'error')
        this.addLog('Error de conexión al buscar investigador', 'error')
      } finally {
        this.loading = false
      }
    },

    async loadWorks() {
      if (!this.researcher) return

      this.loadingWorks = true
      this.works = []
      this.selectedWorks = []

      try {
        this.addLog('Cargando publicaciones del investigador...', 'info')
        
        // Usar el método correcto de la API
        const response = await api.getOrcidWorks(this.researcher.orcid_id)
        
        if (response.success) {
          this.works = response.data
          this.showMessage(`${this.works.length} publicaciones encontradas`, 'success')
          this.addLog(`${this.works.length} publicaciones cargadas correctamente`, 'success')
        } else {
          this.showMessage(response.message || 'No se pudieron cargar las publicaciones', 'error')
          this.addLog('Error al cargar publicaciones', 'error')
        }
      } catch (error) {
        console.error('Error al cargar publicaciones:', error)
        this.showMessage(error.message || 'Error al cargar las publicaciones del investigador', 'error')
        this.addLog('Error de conexión al cargar publicaciones', 'error')
      } finally {
        this.loadingWorks = false
      }
    },

    async syncResearcher() {
      if (!this.researcher) return

      this.syncing = true
      this.addLog('Iniciando sincronización completa...', 'info')

      try {
        // Usar el método correcto de la API
        const response = await api.syncOrcidResearcher(this.researcher.orcid_id)
        
        if (response.success) {
          this.showMessage('Datos del investigador sincronizados exitosamente', 'success')
          this.addLog(`Sincronización completada: ${response.message}`, 'success')
          
          // Mostrar estadísticas si están disponibles
          if (response.stats) {
            const stats = response.stats
            this.addLog(`Estadísticas: ${stats.added} añadidas, ${stats.skipped} existentes, ${stats.failed} fallidas`, 'info')
          }
          
          this.$emit('researcher-synced', this.researcher)
        } else {
          this.showMessage(response.message || 'Error al sincronizar los datos', 'error')
          this.addLog('Error en la sincronización', 'error')
        }
      } catch (error) {
        console.error('Error al sincronizar:', error)
        this.showMessage(error.message || 'Error al sincronizar los datos del investigador', 'error')
        this.addLog('Error de conexión durante la sincronización', 'error')
      } finally {
        this.syncing = false
      }
    },
async addAuthorFromOrcid() {
  if (!this.researcher) {
    this.showMessage('No hay datos del investigador cargados.', 'error')
    return
  }

  this.syncing = true
  this.addLog('Añadiendo autor desde ORCID...', 'info')

  try {
    const response = await api.fetchAuthorFromOrcid(this.researcher.orcid_id)

    if (response.success) {
      this.showMessage('Autor añadido exitosamente.', 'success')
      this.addLog(`Autor creado/actualizado: ${response.author.first_name} ${response.author.last_name}`, 'success')
      this.$emit('author-added', response.author)
    } else {
      this.showMessage(response.error || 'Error al añadir el autor.', 'error')
      this.addLog('Error al añadir el autor.', 'error')
    }
  } catch (error) {
    console.error('Error al añadir autor desde ORCID:', error)
    this.showMessage(error.message || 'Error de conexión al añadir el autor.', 'error')
    this.addLog('Error de conexión al añadir autor.', 'error')
  } finally {
    this.syncing = false
  }
},

    toggleWorkSelection(work) {
      const index = this.selectedWorks.findIndex(w => w.external_id === work.external_id)
      if (index > -1) {
        this.selectedWorks.splice(index, 1)
      } else {
        this.selectedWorks.push(work)
      }
    },

    selectAll() {
      if (this.allSelected) {
        this.selectedWorks = []
      } else {
        this.selectedWorks = [...this.works]
      }
    },

    async addSelectedWorks() {
      if (this.selectedWorks.length === 0) return

      this.adding = true
      this.addLog(`Añadiendo ${this.selectedWorks.length} publicaciones individualmente...`, 'info')

      let successful = 0
      let failed = 0

      try {
        for (const work of this.selectedWorks) {
          try {
            const publicationData = {
              title: work.title,
              type: work.type,
              year: work.year,
              journal: work.journal,
              doi: work.doi,
              url: work.url,
              external_id: work.external_id
            }

            // Usar el método correcto de la API
            const response = await api.createPublicationFromOrcid(publicationData)
            
            if (response.success) {
              successful++
              this.addLog(`✅ Publicación añadida: ${work.title}`, 'success')
            } else {
              failed++
              this.addLog(`❌ Error añadiendo: ${work.title} - ${response.error}`, 'error')
            }
          } catch (error) {
            failed++
            this.addLog(`❌ Error añadiendo: ${work.title} - ${error.message}`, 'error')
          }
        }

        this.showMessage(`${successful} publicaciones añadidas, ${failed} fallidas`, successful > 0 ? 'success' : 'error')
        this.addLog(`Proceso completado: ${successful} exitosas, ${failed} fallidas`, 'info')
        
        if (successful > 0) {
          this.selectedWorks = []
          this.$emit('publications-added', successful)
        }
        
      } catch (error) {
        console.error('Error general:', error)
        this.showMessage('Error al añadir publicaciones', 'error')
        this.addLog('Error general en el proceso', 'error')
      } finally {
        this.adding = false
      }
    },

    async addSelectedWorksBatch() {
      if (this.selectedWorks.length === 0) return

      this.addingBatch = true
      this.addLog(`Añadiendo ${this.selectedWorks.length} publicaciones en lote...`, 'info')

      try {
        const publicationsData = this.selectedWorks.map(work => ({
          title: work.title,
          type: work.type,
          year: work.year,
          journal: work.journal,
          doi: work.doi,
          url: work.url,
          external_id: work.external_id
        }))

        // Usar el método correcto de la API
        const response = await api.createPublicationsBatch(publicationsData)
        
        if (response.success) {
          const created = response.created || []
          const errors = response.errors || []
          
          this.showMessage(`${created.length} publicaciones añadidas en lote`, 'success')
          this.addLog(`Lote completado: ${created.length} exitosas, ${errors.length} fallidas`, 'success')
          
          // Mostrar errores si los hay
          errors.forEach(error => {
            this.addLog(`❌ ${error}`, 'error')
          })
          
          if (created.length > 0) {
            this.selectedWorks = []
            this.$emit('publications-added', created.length)
          }
        } else {
          this.showMessage(response.message || 'Error al añadir publicaciones en lote', 'error')
          this.addLog('Error en el proceso de lote', 'error')
        }
      } catch (error) {
        console.error('Error en lote:', error)
        this.showMessage(error.message || 'Error al añadir publicaciones en lote', 'error')
        this.addLog('Error de conexión en el proceso de lote', 'error')
      } finally {
        this.addingBatch = false
      }
    },

    // Método adicional para usar la función auxiliar de importación completa
    async importAllPublications() {
      if (!this.researcher) return

      this.addingBatch = true
      this.addLog('Iniciando importación completa desde ORCID...', 'info')

      try {
        // Usar el método auxiliar que combina obtener trabajos y crear en lote
        const response = await api.importPublicationsFromOrcid(this.researcher.orcid_id)
        
        if (response.success) {
          this.showMessage(response.message, 'success')
          this.addLog(`Importación completada: ${response.createdPublications} publicaciones creadas de ${response.totalWorks} encontradas`, 'success')
          
          // Mostrar errores si los hay
          if (response.errors && response.errors.length > 0) {
            response.errors.forEach(error => {
              this.addLog(`❌ ${error}`, 'error')
            })
          }
          
          this.$emit('publications-imported', response.createdPublications)
          
          // Recargar las publicaciones disponibles
          await this.loadWorks()
        } else {
          this.showMessage(response.message || 'Error al importar publicaciones', 'error')
          this.addLog('Error en la importación completa', 'error')
        }
      } catch (error) {
        console.error('Error en importación:', error)
        this.showMessage(error.message || 'Error al importar publicaciones desde ORCID', 'error')
        this.addLog('Error de conexión en la importación', 'error')
      } finally {
        this.addingBatch = false
      }
    },

    showMessage(text, type = 'info') {
      this.message = text
      this.messageType = type
      setTimeout(() => {
        this.message = ''
      }, 5000)
    },

    addLog(message, type = 'info') {
      this.operationLogs.push({
        message,
        type,
        timestamp: new Date()
      })
      
      // Mantener solo los últimos 50 logs
      if (this.operationLogs.length > 50) {
        this.operationLogs.shift()
      }
    },

    clearLogs() {
      this.operationLogs = []
    },

    formatTime(timestamp) {
      return timestamp.toLocaleTimeString()
    },

    clearSearch() {
      this.orcidId = ''
      this.researcher = null
      this.works = []
      this.selectedWorks = []
      this.message = ''
      this.clearLogs()
    }
  }
}
</script>

<style scoped>
.orcid-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.orcid-header {
  text-align: center;
  margin-bottom: 3rem;
}

.orcid-header h2 {
  color: #2c3e50;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.orcid-description {
  color: #718096;
  font-size: 1.1rem;
}

/* Search Section */
.search-section {
  margin-bottom: 3rem;
}

.search-form {
  display: flex;
  justify-content: center;
}

.input-group {
  display: flex;
  gap: 1rem;
  width: 100%;
  max-width: 600px;
}

.orcid-input {
  flex: 1;
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 25px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.orcid-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-btn {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.search-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Researcher Info */
.researcher-info {
  margin-bottom: 3rem;
}

.researcher-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.researcher-header h3 {
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.researcher-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.orcid-badge, .email {
  padding: 0.5rem 1rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 20px;
  font-size: 0.9rem;
  color: #667eea;
}

.affiliation {
  color: #718096;
  font-style: italic;
  margin-bottom: 1.5rem;
}

.researcher-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.load-works {
  background: linear-gradient(135deg, #48bb78, #38a169);
  color: white;
}

.sync-btn {
  background: linear-gradient(135deg, #ed8936, #dd6b20);
  color: white;
}

.select-all {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.add-selected {
  background: linear-gradient(135deg, #48bb78, #38a169);
  color: white;
}

.add-batch {
  background: linear-gradient(135deg, #9f7aea, #805ad5);
  color: white;
}

.action-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Works Section */
.works-section {
  margin-bottom: 3rem;
}

.works-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.works-header h3 {
  color: #2c3e50;
  font-size: 1.5rem;
}

.works-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.works-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.work-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.work-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.work-card.selected {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}

.work-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
}

.work-checkbox {
  margin-top: 0.25rem;
  transform: scale(1.2);
}

.work-title {
  color: #2c3e50;
  font-size: 1.1rem;
  line-height: 1.3;
  margin: 0;
}

.work-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.work-type, .work-year {
  padding: 0.25rem 0.75rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 15px;
  font-size: 0.8rem;
  color: #667eea;
}

.work-details {
  font-size: 0.9rem;
  color: #4a5568;
  line-height: 1.4;
}

.work-details p {
  margin-bottom: 0.5rem;
}

.work-details a {
  color: #667eea;
  text-decoration: none;
}

.work-details a:hover {
  text-decoration: underline;
}

/* Messages */
.message {
  padding: 1rem;
  border-radius: 10px;
  margin-top: 2rem;
  text-align: center;
  font-weight: 500;
}

.message.success {
  background: rgba(72, 187, 120, 0.1);
  color: #2f855a;
  border: 1px solid rgba(72, 187, 120, 0.2);
}

.message.error {
  background: rgba(245, 101, 101, 0.1);
  color: #c53030;
  border: 1px solid rgba(245, 101, 101, 0.2);
}

.message.info {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border: 1px solid rgba(102, 126, 234, 0.2);
}

/* Logs Section */
.logs-section {
  margin-top: 3rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.logs-section h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.logs-container {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1rem;
}

.log-item {
  display: flex;
  gap: 1rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f7fafc;
  font-size: 0.9rem;
}

.log-item:last-child {
  border-bottom: none;
}

.log-timestamp {
  color: #718096;
  font-family: monospace;
  min-width: 80px;
}

.log-message {
  flex: 1;
}

.log-item.success .log-message {
  color: #2f855a;
}

.log-item.error .log-message {
  color: #c53030;
}

.log-item.info .log-message {
  color: #4a5568;
}
.action-btn.add-author-btn {
  background-color: #2d9cdb;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-weight: 500;
  margin-left: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.action-btn.add-author-btn:hover {
  background-color: #238ac9;
}
.action-btn.add-author-btn:disabled {
  background-color: #a0cfee;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .orcid-container {
    padding: 1rem;
  }

  .input-group {
    flex-direction: column;
  }

  .works-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .works-grid {
    grid-template-columns: 1fr;
  }

  .work-card {
    padding: 1rem;
  }

  .researcher-actions, .works-actions {
    justify-content: center;
  }
}
</style>