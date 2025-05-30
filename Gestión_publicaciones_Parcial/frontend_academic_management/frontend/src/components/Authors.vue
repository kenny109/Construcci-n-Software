<template>
  <div class="authors">
    <div class="authors-header">
      <h1>Gestión de Autores</h1>
      <button @click="showCreateModal = true" class="btn btn-primary">
        Agregar Autor
      </button>
    </div>
    
    <div class="authors-filters container">
      <div class="filters-row">
        <div class="search-box">
          <input
            v-model="searchTerm"
            type="text"
            placeholder="Buscar por nombre, email o institución..."
            class="form-input"
          />
        </div>
        <div class="filter-actions">
          <button @click="loadAuthors" class="btn btn-secondary">
            Actualizar
          </button>
        </div>
      </div>
    </div>
    
    <div class="authors-content container">
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Cargando autores...</p>
      </div>
      
      <div v-else-if="filteredAuthors.length === 0" class="empty-state">
        <h3>No se encontraron autores</h3>
        <p>{{ searchTerm ? 'No hay autores que coincidan con tu búsqueda' : 'Aún no hay autores registrados' }}</p>
      </div>
      
      <div v-else class="authors-grid grid grid-3">
        <div
          v-for="author in filteredAuthors"
          :key="author.id"
          class="author-card card"
        >
          <div class="author-header">
            <div class="author-avatar">
              {{ getInitials(author.first_name, author.last_name) }}
            </div>
            <div class="author-info">
              <h3>{{ author.first_name }} {{ author.last_name }}</h3>
              <p class="author-email">{{ author.email || 'Sin email' }}</p>
            </div>
          </div>
          
          <div class="author-details">
            <div class="detail-item">
              <strong>Institución:</strong>
              <span>{{ author.institution || 'No especificada' }}</span>
            </div>
            <div class="detail-item" v-if="author.orcid_id">
              <strong>ORCID:</strong>
              <span>{{ author.orcid_id }}</span>
            </div>
            <div class="detail-item">
              <strong>Registrado:</strong>
              <span>{{ formatDate(author.created_at) }}</span>
            </div>
          </div>
          
          <div class="author-actions">
            <button
              @click="editAuthor(author)"
              class="btn btn-sm btn-secondary"
            >
              Editar
            </button>
            <button
              @click="deleteAuthor(author)"
              class="btn btn-sm btn-danger"
            >
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal para crear/editar autor -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click="closeModals">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h2>{{ showCreateModal ? 'Crear Nuevo Autor' : 'Editar Autor' }}</h2>
          <button @click="closeModals" class="modal-close">×</button>
        </div>
        
        <form @submit.prevent="saveAuthor" class="modal-body">
          <div class="form-group">
            <label class="form-label">Nombre *</label>
            <input
              v-model="authorForm.first_name"
              type="text"
              class="form-input"
              required
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Apellido *</label>
            <input
              v-model="authorForm.last_name"
              type="text"
              class="form-input"
              required
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Email</label>
            <input
              v-model="authorForm.email"
              type="email"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">Institución</label>
            <input
              v-model="authorForm.institution"
              type="text"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label class="form-label">ORCID ID</label>
            <input
              v-model="authorForm.orcid_id"
              type="text"
              class="form-input"
              placeholder="0000-0000-0000-0000"
            />
          </div>
          
          <div class="modal-actions">
            <button type="button" @click="closeModals" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" :disabled="saving" class="btn btn-primary">
              {{ saving ? 'Guardando...' : (showCreateModal ? 'Crear' : 'Actualizar') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

export default {
  name: 'Authors',
  setup() {
    const authors = ref([])
    const searchTerm = ref('')
    const loading = ref(false)
    const saving = ref(false)
    
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const editingAuthor = ref(null)
    
    const authorForm = ref({
      first_name: '',
      last_name: '',
      email: '',
      institution: '',
      orcid_id: ''
    })
    
    const filteredAuthors = computed(() => {
      if (!searchTerm.value) return authors.value
      
      const term = searchTerm.value.toLowerCase()
      return authors.value.filter(author =>
        `${author.first_name} ${author.last_name}`.toLowerCase().includes(term) ||
        (author.email && author.email.toLowerCase().includes(term)) ||
        (author.institution && author.institution.toLowerCase().includes(term))
      )
    })
    
    const loadAuthors = async () => {
      loading.value = true
      try {
        const response = await api.get('/authors')
        authors.value = response.data
      } catch (error) {
        console.error('Error loading authors:', error)
        alert('Error al cargar autores')
      } finally {
        loading.value = false
      }
    }
    
    const resetForm = () => {
      authorForm.value = {
        first_name: '',
        last_name: '',
        email: '',
        institution: '',
        orcid_id: ''
      }
    }
    
    const closeModals = () => {
      showCreateModal.value = false
      showEditModal.value = false
      editingAuthor.value = null
      resetForm()
    }
    
    const editAuthor = (author) => {
      editingAuthor.value = author
      authorForm.value = { ...author }
      showEditModal.value = true
    }
    
    const saveAuthor = async () => {
      saving.value = true
      try {
        if (showCreateModal.value) {
          await api.post('/authors', authorForm.value)
        } else {
          await api.put(`/authors/${editingAuthor.value.id}`, authorForm.value)
        }
        
        await loadAuthors()
        closeModals()
        alert(showCreateModal.value ? 'Autor creado exitosamente' : 'Autor actualizado exitosamente')
      } catch (error) {
        console.error('Error saving author:', error)
        alert('Error al guardar autor')
      } finally {
        saving.value = false
      }
    }
    
    const deleteAuthor = async (author) => {
      if (!confirm(`¿Está seguro de eliminar al autor ${author.first_name} ${author.last_name}?`)) {
        return
      }
      
      try {
        await api.delete(`/authors/${author.id}`)
        await loadAuthors()
        alert('Autor eliminado exitosamente')
      } catch (error) {
        console.error('Error deleting author:', error)
        alert('Error al eliminar autor')
      }
    }
    
    const getInitials = (firstName, lastName) => {
      return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase()
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString('es-ES')
    }
    
    onMounted(() => {
      loadAuthors()
    })
    
    return {
      authors,
      searchTerm,
      loading,
      saving,
      showCreateModal,
      showEditModal,
      authorForm,
      filteredAuthors,
      loadAuthors,
      closeModals,
      editAuthor,
      saveAuthor,
      deleteAuthor,
      getInitials,
      formatDate
    }
  }
}
</script>

<style scoped>
.authors-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.authors-header h1 {
  font-size: 2rem;
  color: #1f2937;
}

.authors-filters {
  margin-bottom: 2rem;
}

.filters-row {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-box {
  flex: 1;
}

.author-card {
  padding: 1.5rem;
}

.author-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.author-avatar {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.1rem;
}

.author-info h3 {
  font-size: 1.1rem;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.author-email {
  color: #6b7280;
  font-size: 0.9rem;
}

.author-details {
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.detail-item strong {
  color: #374151;
  min-width: 80px;
}

.detail-item span {
  color: #6b7280;
  text-align: right;
}

.author-actions {
  display: flex;
  gap: 0.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #6b7280;
}

.empty-state h3 {
  margin-bottom: 0.5rem;
  color: #374151;
}

/* Modal styles */
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
  padding: 1rem;
}

.modal {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
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

.modal-close {
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

.modal-close:hover {
  color: #374151;
}

.modal-body {
  padding: 1.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

@media (max-width: 768px) {
  .authors-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .filters-row {
    flex-direction: column;
  }
  
  .authors-grid {
    grid-template-columns: 1fr;
  }
}
</style>