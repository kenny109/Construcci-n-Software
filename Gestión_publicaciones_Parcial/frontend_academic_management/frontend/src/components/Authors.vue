<template>
  <div class="authors">
    <div class="page-header">
      <div class="header-content">
        <h1>Gestión de Autores</h1>
        <p>Administra los autores del sistema académico</p>
      </div>
      <button @click="showCreateModal = true" class="btn btn-primary">
        + Nuevo Autor
      </button>
    </div>
    
    <div v-if="message" :class="['alert', messageType === 'success' ? 'alert-success' : 'alert-error']">
      {{ message }}
    </div>
    
    <div class="authors-container">
      <div v-if="isLoading" class="loading">
        Cargando autores...
      </div>
      
      <div v-else-if="authors.length === 0" class="empty-state">
        <h3>No hay autores registrados</h3>
        <p>Comienza agregando el primer autor al sistema</p>
        <button @click="showCreateModal = true" class="btn btn-primary">
          Crear Primer Autor
        </button>
      </div>
      
      <div v-else class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Email</th>
              <th>Institución</th>
              <th>ORCID ID</th>
              <th>Fecha Creación</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="author in authors" :key="author.id">
              <td>{{ author.first_name }} {{ author.last_name }}</td>
              <td>{{ author.email || 'N/A' }}</td>
              <td>{{ author.institution || 'N/A' }}</td>
              <td>{{ author.orcid_id || 'N/A' }}</td>
              <td>{{ formatDate(author.created_at) }}</td>
              <td class="actions">
                <button @click="editAuthor(author)" class="btn btn-secondary btn-sm">
                  Editar
                </button>
                <button @click="deleteAuthor(author.id)" class="btn btn-danger btn-sm">
                  Eliminar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Modal Create/Edit -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">
            {{ showCreateModal ? 'Crear Nuevo Autor' : 'Editar Autor' }}
          </h3>
          <button @click="closeModal" class="btn-close">&times;</button>
        </div>
        
        <form @submit.prevent="saveAuthor">
          <div v-if="formError" class="alert alert-error">
            {{ formError }}
          </div>
          
          <div class="form-group">
            <label class="form-label">Nombre *</label>
            <input
              v-model="form.first_name"
              type="text"
              class="form-control"
              required
              placeholder="Nombre del autor"
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Apellido *</label>
            <input
              v-model="form.last_name"
              type="text"
              class="form-control"
              required
              placeholder="Apellido del autor"
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Email</label>
            <input
              v-model="form.email"
              type="email"
              class="form-control"
              placeholder="email@ejemplo.com"
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Institución</label>
            <input
              v-model="form.institution"
              type="text"
              class="form-control"
              placeholder="Nombre de la institución"
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">ORCID ID</label>
            <input
              v-model="form.orcid_id"
              type="text"
              class="form-control"
              placeholder="0000-0000-0000-0000"
              pattern="[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}"
            >
          </div>
          
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary" :disabled="isSaving">
              {{ isSaving ? 'Guardando...' : (showCreateModal ? 'Crear' : 'Actualizar') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import apiService from '../services/api'

export default {
  name: 'Authors',
  setup() {
    const authors = ref([])
    const isLoading = ref(false)
    const isSaving = ref(false)
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const editingAuthor = ref(null)
    const message = ref('')
    const messageType = ref('success')
    const formError = ref('')
    
    const form = ref({
      first_name: '',
      last_name: '',
      email: '',
      institution: '',
      orcid_id: ''
    })
    
    const loadAuthors = async () => {
      isLoading.value = true
      try {
        authors.value = await apiService.getAuthors()
      } catch (error) {
        showMessage('Error al cargar los autores: ' + error.message, 'error')
      } finally {
        isLoading.value = false
      }
    }
    
    const saveAuthor = async () => {
      isSaving.value = true
      formError.value = ''
      
      try {
        if (showCreateModal.value) {
          await apiService.createAuthor(form.value)
          showMessage('Autor creado exitosamente', 'success')
        } else {
          await apiService.updateAuthor(editingAuthor.value.id, form.value)
          showMessage('Autor actualizado exitosamente', 'success')
        }
        
        closeModal()
        loadAuthors()
      } catch (error) {
        formError.value = 'Error al guardar: ' + error.message
      } finally {
        isSaving.value = false
      }
    }
    
    const editAuthor = (author) => {
      editingAuthor.value = author
      form.value = {
        first_name: author.first_name,
        last_name: author.last_name,
        email: author.email || '',
        institution: author.institution || '',
        orcid_id: author.orcid_id || ''
      }
      showEditModal.value = true
    }
    
    const deleteAuthor = async (id) => {
      if (!confirm('¿Estás seguro de que deseas eliminar este autor?')) {
        return
      }
      
      try {
        await apiService.deleteAuthor(id)
        showMessage('Autor eliminado exitosamente', 'success')
        loadAuthors()
      } catch (error) {
        showMessage('Error al eliminar autor: ' + error.message, 'error')
      }
    }
    
    const closeModal = () => {
      showCreateModal.value = false
      showEditModal.value = false
      editingAuthor.value = null
      formError.value = ''
      form.value = {
        first_name: '',
        last_name: '',
        email: '',
        institution: '',
        orcid_id: ''
      }
    }
    
    const showMessage = (msg, type) => {
      message.value = msg
      messageType.value = type
      setTimeout(() => {
        message.value = ''
      }, 5000)
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('es-ES')
    }
    
    onMounted(() => {
      loadAuthors()
    })
    
    return {
      authors,
      isLoading,
      isSaving,
      showCreateModal,
      showEditModal,
      form,
      message,
      messageType,
      formError,
      saveAuthor,
      editAuthor,
      deleteAuthor,
      closeModal,
      formatDate
    }
  }
}
</script>

<style scoped>
.authors {
  padding: 2rem 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-content h1 {
  font-size: 2.2rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.header-content p {
  color: #666;
  margin: 0.5rem 0 0 0;
}

.authors-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  overflow: hidden;
}

.table-container {
  overflow-x: auto;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-state h3 {
  color: #333;
  margin-bottom: 1rem;
}

.empty-state p {
  color: #666;
  margin-bottom: 2rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.9rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .actions {
    flex-direction: column;
    width: 100%;
  }
  
  .btn-sm {
    width: 100%;
  }
}
</style>