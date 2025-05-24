<template>
  <div class="container">
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">📚 Gestión de Autores</h2>
        <p class="card-subtitle">Administra los autores de la biblioteca</p>
      </div>
      
      <div style="margin-bottom: 20px;">
        <button @click="showModal = true" class="btn btn-primary">
          ➕ Nuevo Autor
        </button>
      </div>
      
      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>
      
      <div v-if="success" class="alert alert-success">
        {{ success }}
      </div>
      
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Cargando autores...</p>
      </div>
      
      <div v-else-if="autores.length === 0" class="loading">
        <p>No hay autores registrados</p>
      </div>
      
      <div v-else class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre Completo</th>
              <th>Nacionalidad</th>
              <th>Fecha de Nacimiento</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="autor in autores" :key="autor.autor_id">
              <td>{{ autor.autor_id }}</td>
              <td>{{ autor.nombre }} {{ autor.apellido }}</td>
              <td>{{ autor.nacionalidad || 'No especificada' }}</td>
              <td>{{ formatDate(autor.fecha_nacimiento) }}</td>
              <td>
                <button 
                  @click="editAutor(autor)" 
                  class="btn btn-warning btn-sm"
                  style="margin-right: 10px;"
                >
                  ✏️ Editar
                </button>
                <button 
                  @click="deleteAutor(autor)" 
                  class="btn btn-danger btn-sm"
                >
                  🗑️ Eliminar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Modal para crear/editar autor -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3 class="modal-title">
            {{ isEditing ? 'Editar Autor' : 'Nuevo Autor' }}
          </h3>
          <button @click="closeModal" class="modal-close">&times;</button>
        </div>
        
        <form @submit.prevent="saveAutor">
          <div class="form-group">
            <label class="form-label">Nombre *</label>
            <input 
              v-model="currentAutor.nombre"
              type="text" 
              class="form-input"
              placeholder="Ingresa el nombre"
              required
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Apellido *</label>
            <input 
              v-model="currentAutor.apellido"
              type="text" 
              class="form-input"
              placeholder="Ingresa el apellido"
              required
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Nacionalidad</label>
            <input 
              v-model="currentAutor.nacionalidad"
              type="text" 
              class="form-input"
              placeholder="Ingresa la nacionalidad"
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Fecha de Nacimiento</label>
            <input 
              v-model="currentAutor.fecha_nacimiento"
              type="date" 
              class="form-input"
            >
          </div>
          
          <div class="modal-footer">
            <button type="button" @click="closeModal" class="btn btn-secondary">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loadingAction">
              {{ loadingAction ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'AutorList',
  data() {
    return {
      autores: [],
      showModal: false,
      isEditing: false,
      currentAutor: {
        autor_id: null,
        nombre: '',
        apellido: '',
        nacionalidad: '',
        fecha_nacimiento: ''
      },
      loading: false,
      loadingAction: false,
      error: '',
      success: ''
    }
  },
  async created() {
    await this.loadAutores()
  },
  methods: {
    async loadAutores() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await api.getAutores()
        this.autores = response.data || []
      } catch (error) {
        console.error('Error cargando autores:', error)
        this.error = 'Error al cargar los autores'
      } finally {
        this.loading = false
      }
    },
    
    editAutor(autor) {
      this.isEditing = true
      this.currentAutor = { ...autor }
      this.showModal = true
    },
    
    async deleteAutor(autor) {
      if (!confirm(`¿Estás seguro de eliminar al autor ${autor.nombre} ${autor.apellido}?`)) {
        return
      }
      
      try {
        await api.deleteAutor(autor.autor_id)
        this.success = 'Autor eliminado con éxito'
        await this.loadAutores()
        this.clearMessages()
      } catch (error) {
        console.error('Error eliminando autor:', error)
        this.error = 'Error al eliminar el autor'
        this.clearMessages()
      }
    },
    
    async saveAutor() {
      if (!this.currentAutor.nombre.trim() || !this.currentAutor.apellido.trim()) {
        this.error = 'El nombre y apellido son requeridos'
        this.clearMessages()
        return
      }
      
      this.loadingAction = true
      this.error = ''
      
      try {
        if (this.isEditing) {
          await api.updateAutor(this.currentAutor)
          this.success = 'Autor actualizado con éxito'
        } else {
          await api.createAutor(this.currentAutor)
          this.success = 'Autor creado con éxito'
        }
        
        this.closeModal()
        await this.loadAutores()
        this.clearMessages()
      } catch (error) {
        console.error('Error guardando autor:', error)
        this.error = error.response?.data?.error || 'Error al guardar el autor'
        this.clearMessages()
      } finally {
        this.loadingAction = false
      }
    },
    
    closeModal() {
      this.showModal = false
      this.isEditing = false
      this.currentAutor = {
        autor_id: null,
        nombre: '',
        apellido: '',
        nacionalidad: '',
        fecha_nacimiento: ''
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return 'No especificada'
      const date = new Date(dateString)
      return date.toLocaleDateString('es-ES')
    },
    
    clearMessages() {
      setTimeout(() => {
        this.error = ''
        this.success = ''
      }, 3000)
    }
  }
}
</script>