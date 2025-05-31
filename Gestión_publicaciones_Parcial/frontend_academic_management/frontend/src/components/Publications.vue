<template>
  <div class="publications">
    <div class="publications-header">
      <h1>Gestión de Publicaciones</h1>
      <button @click="openCreateModal" class="btn btn-primary">
        Nueva Publicación
      </button>
    </div>

    <!-- Filtros -->
    <div class="filters-section card">
      <h3>Filtros</h3>
      <div class="filters-grid grid grid-3">
        <div class="form-group">
          <label class="form-label">Buscar por título</label>
          <input
            v-model="filters.search"
            type="text"
            class="form-input"
            placeholder="Título de la publicación"
          />
        </div>
        <div class="form-group">
          <label class="form-label">Tipo de publicación</label>
          <select v-model="filters.type" class="form-input">
            <option value="">Todos los tipos</option>
            <option v-for="type in publicationTypes" :key="type.id" :value="type.id">
              {{ type.name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Año</label>
          <input
            v-model="filters.year"
            type="number"
            class="form-input"
            placeholder="2024"
          />
        </div>
      </div>
      <div class="filters-actions">
        <button @click="applyFilters" class="btn btn-secondary">Aplicar Filtros</button>
        <button @click="clearFilters" class="btn btn-secondary">Limpiar</button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
    </div>

    <!-- Tabla de publicaciones -->
    <div v-else class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>Título</th>
            <th>Tipo</th>
            <th>Fecha</th>
            <th>Autores</th>
            <th>Revista/Conferencia</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredPublications.length === 0">
            <td colspan="6" class="text-center">No hay publicaciones registradas</td>
          </tr>
          <tr v-for="publication in filteredPublications" :key="publication.id">
            <td>
              <div class="publication-title">
                {{ publication.title }}
                <div v-if="publication.doi" class="publication-doi">
                  DOI: {{ publication.doi }}
                </div>
              </div>
            </td>
            <td>
              <span class="type-badge">
                {{ getPublicationType(publication.publication_type_id) }}
              </span>
            </td>
            <td>{{ formatDate(publication.publication_date) }}</td>
            <td>
              <div class="authors-list">
                <span v-for="(author, index) in getPublicationAuthors(publication.id)" :key="author.id">
                  {{ author.first_name }} {{ author.last_name }}<span v-if="index < getPublicationAuthors(publication.id).length - 1">, </span>
                </span>
              </div>
            </td>
            <td>
              {{ getPublicationVenue(publication) }}
            </td>
            <td>
              <div class="action-buttons">
                <button @click="viewPublication(publication)" class="btn btn-sm btn-secondary">
                  Ver
                </button>
                <button @click="editPublication(publication)" class="btn btn-sm btn-primary">
                  Editar
                </button>
                <button @click="deletePublication(publication)" class="btn btn-sm btn-danger">
                  Eliminar
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal para crear/editar publicación -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ editingPublication ? 'Editar Publicación' : 'Nueva Publicación' }}</h2>
          <button @click="closeModal" class="btn-close">&times;</button>
        </div>
        
        <form @submit.prevent="savePublication" class="modal-body">
          <div class="form-group">
            <label class="form-label">Título *</label>
            <input
              v-model="currentPublication.title"
              type="text"
              class="form-input"
              required
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Resumen</label>
            <textarea
              v-model="currentPublication.abstract"
              class="form-input form-textarea"
              rows="4"
            ></textarea>
          </div>
          
          <div class="grid grid-2">
            <div class="form-group">
              <label class="form-label">Tipo de Publicación *</label>
              <select v-model="currentPublication.publication_type_id" class="form-input" required>
                <option value="">Seleccionar tipo</option>
                <option v-for="type in publicationTypes" :key="type.id" :value="type.id">
                  {{ type.name }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label">Fecha de Publicación</label>
              <input
                v-model="currentPublication.publication_date"
                type="date"
                class="form-input"
              />
            </div>
          </div>
          
          <div class="grid grid-2">
            <div class="form-group">
              <label class="form-label">DOI</label>
              <input
                v-model="currentPublication.doi"
                type="text"
                class="form-input"
                placeholder="10.1000/182"
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">URL</label>
              <input
                v-model="currentPublication.url"
                type="url"
                class="form-input"
                placeholder="https://..."
              />
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-label">Revista</label>
            <select v-model="currentPublication.journal_id" class="form-input">
              <option value="">Seleccionar revista</option>
              <option v-for="journal in journals" :key="journal.id" :value="journal.id">
                {{ journal.name }}
              </option>
            </select>
          </div>
          
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary">
              {{ editingPublication ? 'Actualizar' : 'Crear' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import api from '../services/api'

export default {
  name: 'Publications',
  setup() {
    const publications = ref([])
    const publicationTypes = ref([])
    const journals = ref([])
    const authors = ref([])
    const publicationAuthors = ref([])
    const loading = ref(false)
    const showModal = ref(false)
    const editingPublication = ref(null)
    
    const filters = ref({
      search: '',
      type: '',
      year: ''
    })
    
    const currentPublication = ref({
      title: '',
      abstract: '',
      doi: '',
      url: '',
      publication_date: '',
      publication_type_id: '',
      journal_id: '',
      conference_id: ''
    })
    
    const filteredPublications = computed(() => {
      let filtered = publications.value
      
      if (filters.value.search) {
        filtered = filtered.filter(pub => 
          pub.title.toLowerCase().includes(filters.value.search.toLowerCase())
        )
      }
      
      if (filters.value.type) {
        filtered = filtered.filter(pub => pub.publication_type_id === filters.value.type)
      }
      
      if (filters.value.year) {
        filtered = filtered.filter(pub => {
          if (!pub.publication_date) return false
          const pubYear = new Date(pub.publication_date).getFullYear()
          return pubYear.toString() === filters.value.year
        })
      }
      
      return filtered
    })
    
    const loadPublications = async () => {
      loading.value = true
      try {
        const response = await api.get('/publications')
        publications.value = response.data
      } catch (error) {
        console.error('Error loading publications:', error)
      } finally {
        loading.value = false
      }
    }
    
    const loadPublicationTypes = async () => {
      try {
        const response = await api.get('/publication-types')
        publicationTypes.value = response.data
      } catch (error) {
        console.error('Error loading publication types:', error)
      }
    }
    
    const loadJournals = async () => {
      try {
        const response = await api.get('/journals')
        journals.value = response.data
      } catch (error) {
        console.error('Error loading journals:', error)
      }
    }
    
    const loadAuthors = async () => {
      try {
        const response = await api.get('/authors')
        authors.value = response.data
      } catch (error) {
        console.error('Error loading authors:', error)
      }
    }
    
    const loadPublicationAuthors = async () => {
      try {
        const response = await api.get('/publication-authors')
        publicationAuthors.value = response.data
      } catch (error) {
        console.error('Error loading publication authors:', error)
      }
    }
    
    const getPublicationType = (typeId) => {
      const type = publicationTypes.value.find(t => t.id === typeId)
      return type ? type.name : 'N/A'
    }
    
    const getPublicationVenue = (publication) => {
      if (publication.journal_id) {
        const journal = journals.value.find(j => j.id === publication.journal_id)
        return journal ? journal.name : 'N/A'
      }
      return 'N/A'
    }
    
    const getPublicationAuthors = (publicationId) => {
      const pubAuthors = publicationAuthors.value.filter(pa => pa.publication_id === publicationId)
      return pubAuthors.map(pa => {
        const author = authors.value.find(a => a.id === pa.author_id)
        return author || { first_name: 'N/A', last_name: '' }
      }).sort((a, b) => a.author_order - b.author_order)
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Sin fecha'
      return new Date(dateString).toLocaleDateString('es-ES')
    }
    
    const openCreateModal = () => {
      editingPublication.value = null
      currentPublication.value = {
        title: '',
        abstract: '',
        doi: '',
        url: '',
        publication_date: '',
        publication_type_id: '',
        journal_id: '',
        conference_id: ''
      }
      showModal.value = true
    }
    
    const editPublication = (publication) => {
      editingPublication.value = publication
      currentPublication.value = { ...publication }
      showModal.value = true
    }
    
    const closeModal = () => {
      showModal.value = false
      editingPublication.value = null
    }
    
    const savePublication = async () => {
      try {
        if (editingPublication.value) {
          await api.put(`/publications/${editingPublication.value.id}`, currentPublication.value)
        } else {
          await api.post('/publications', currentPublication.value)
        }
        await loadPublications()
        closeModal()
      } catch (error) {
        console.error('Error saving publication:', error)
        alert('Error al guardar la publicación')
      }
    }
    
    const deletePublication = async (publication) => {
      if (confirm(`¿Está seguro de eliminar la publicación "${publication.title}"?`)) {
        try {
          await api.delete(`/publications/${publication.id}`)
          await loadPublications()
        } catch (error) {
          console.error('Error deleting publication:', error)
          alert('Error al eliminar la publicación')
        }
      }
    }
    
    const viewPublication = (publication) => {
      alert(`Título: ${publication.title}\nDOI: ${publication.doi || 'N/A'}\nResumen: ${publication.abstract || 'Sin resumen'}`)
    }
    
    const applyFilters = () => {
      // Los filtros se aplican automáticamente por computed
    }
    
    const clearFilters = () => {
      filters.value = {
        search: '',
        type: '',
        year: ''
      }
    }
    
    onMounted(() => {
      loadPublications()
      loadPublicationTypes()
      loadJournals()
      loadAuthors()
      loadPublicationAuthors()
    })
    
    return {
      publications,
      publicationTypes,
      journals,
      authors,
      loading,
      showModal,
      editingPublication,
      currentPublication,
      filters,
      filteredPublications,
      getPublicationType,
      getPublicationVenue,
      getPublicationAuthors,
      formatDate,
      openCreateModal,
      editPublication,
      closeModal,
      savePublication,
      deletePublication,
      viewPublication,
      applyFilters,
      clearFilters
    }
  }
}
</script>

<style scoped>
.publications-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.publications-header h1 {
  font-size: 2rem;
  color: #1f2937;
}

.filters-section {
  margin-bottom: 2rem;
}

.filters-section h3 {
  margin-bottom: 1rem;
  color: #374151;
}

.filters-grid {
  margin-bottom: 1rem;
}

.filters-actions {
  display: flex;
  gap: 1rem;
}

.publication-title {
  line-height: 1.4;
}

.publication-doi {
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.type-badge {
  background-color: #e5e7eb;
  color: #374151;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.authors-list {
  font-size: 0.9rem;
  color: #4b5563;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  font-size: 1.25rem;
  color: #1f2937;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  color: #374151;
}

.modal-body {
  padding: 1.5rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

@media (max-width: 768px) {
  .publications-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .filters-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .modal-content {
    width: 95%;
    margin: 1rem;
  }
}
</style>