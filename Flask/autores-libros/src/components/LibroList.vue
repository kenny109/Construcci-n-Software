<template>
  <div class="container">
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">📖 Gestión de Libros</h2>
        <p class="card-subtitle">Administra los libros de la biblioteca</p>
      </div>
      
      <div style="margin-bottom: 20px;">
        <button @click="showModal = true" class="btn btn-primary">
          ➕ Nuevo Libro
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
        <p>Cargando libros...</p>
      </div>
      
      <div v-else-if="libros.length === 0" class="loading">
        <p>No hay libros registrados</p>
      </div>
      
      <div v-else class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Título</th>
              <th>Año</th>
              <th>Autores</th>
              <th>Géneros</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="libro in libros" :key="libro.libro_id">
              <td>{{ libro.libro_id }}</td>
              <td>{{ libro.titulo }}</td>
              <td>{{ libro.anio_publicacion || 'N/A' }}</td>
              <td>
                <span v-if="libro.autores && libro.autores.length">
                  <span v-for="(autor, index) in libro.autores" :key="autor.autor_id">
                    {{ autor.nombre }} {{ autor.apellido }}
                    <span v-if="index < libro.autores.length - 1">, </span>
                  </span>
                </span>
                <span v-else>Sin autores</span>
              </td>
              <td>
                <span v-if="libro.generos && libro.generos.length">
                  <span v-for="(genero, index) in libro.generos" :key="genero.genero_id">
                    {{ genero.nombre }}
                    <span v-if="index < libro.generos.length - 1">, </span>
                  </span>
                </span>
                <span v-else>Sin géneros</span>
              </td>
              <td>
                <button 
                  @click="editLibro(libro)" 
                  class="btn btn-warning btn-sm"
                  style="margin-right: 10px;"
                >
                  ✏️ Editar
                </button>
                <button 
                  @click="deleteLibro(libro)" 
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
    
    <!-- Modal para crear/editar libro -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <div class="modal-header">
          <h3 class="modal-title">
            {{ isEditing ? 'Editar Libro' : 'Nuevo Libro' }}
          </h3>
          <button @click="closeModal" class="modal-close">&times;</button>
        </div>
        
        <form @submit.prevent="saveLibro">
          <div class="form-group">
            <label class="form-label">Título *</label>
            <input 
              v-model="currentLibro.titulo"
              type="text" 
              class="form-input"
              placeholder="Ingresa el título del libro"
              required
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Año de Publicación</label>
            <input 
              v-model="currentLibro.anio_publicacion"
              type="number" 
              class="form-input"
              placeholder="Ingresa el año"
              min="1000"
              max="2030"
            >
          </div>
          
          <div class="form-group">
            <label class="form-label">Autores *</label>
            <div style="max-height: 150px; overflow-y: auto; border: 1px solid #e1e5e9; border-radius: 5px; padding: 10px;">
              <div v-for="autor in autores" :key="autor.autor_id" style="margin-bottom: 5px;">
                <label style="display: flex; align-items: center; font-weight: normal;">
                  <input 
                    type="checkbox" 
                    :value="autor.autor_id"
                    v-model="currentLibro.autores_ids"
                    class="form-checkbox"
                  >
                  {{ autor.nombre }} {{ autor.apellido }}
                </label>
              </div>
            </div>
            <small v-if="autores.length === 0" style="color: #666;">
              No hay autores disponibles. <router-link to="/autores">Crear autores</router-link>
            </small>
          </div>
          
          <div class="form-group">
            <label class="form-label">Géneros</label>
            <div style="max-height: 150px; overflow-y: auto; border: 1px solid #e1e5e9; border-radius: 5px; padding: 10px;">
              <div v-for="genero in generos" :key="genero.genero_id" style="margin-bottom: 5px;">
                <label style="display: flex; align-items: center; font-weight: normal;">
                  <input 
                    type="checkbox" 
                    :value="genero.genero_id"
                    v-model="currentLibro.generos_ids"
                    class="form-checkbox"
                  >
                  {{ genero.nombre }}
                </label>
              </div>
            </div>
            <small v-if="generos.length === 0" style="color: #666;">
              No hay géneros disponibles. <router-link to="/generos">Crear géneros</router-link>
            </small>
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
  name: 'LibroList',
  data() {
    return {
      libros: [],
      autores: [],
      generos: [],
      showModal: false,
      isEditing: false,
      currentLibro: {
        libro_id: null,
        titulo: '',
        anio_publicacion: null,
        autores_ids: [],
        generos_ids: []
      },
      loading: false,
      loadingAction: false,
      error: '',
      success: ''
    }
  },
  async created() {
    await Promise.all([
      this.loadLibros(),
      this.loadAutores(),
      this.loadGeneros()
    ])
  },
  methods: {
    async loadLibros() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await api.getLibros()
        this.libros = response.data || []
      } catch (error) {
        console.error('Error cargando libros:', error)
        this.error = 'Error al cargar los libros'
      } finally {
        this.loading = false
      }
    },
    
    async loadAutores() {
      try {
        const response = await api.getAutores()
        this.autores = response.data || []
      } catch (error) {
        console.error('Error cargando autores:', error)
      }
    },
    
    async loadGeneros() {
      try {
        const response = await api.getGeneros()
        this.generos = response.data || []
      } catch (error) {
        console.error('Error cargando géneros:', error)
      }
    },
    
    editLibro(libro) {
      this.isEditing = true
      this.currentLibro = {
        libro_id: libro.libro_id,
        titulo: libro.titulo,
        anio_publicacion: libro.anio_publicacion,
        autores_ids: libro.autores ? libro.autores.map(a => a.autor_id) : [],
        generos_ids: libro.generos ? libro.generos.map(g => g.genero_id) : []
      }
      this.showModal = true
    },
    
    async deleteLibro(libro) {
      if (!confirm(`¿Estás seguro de eliminar el libro "${libro.titulo}"?`)) {
        return
      }
      
      try {
        await api.deleteLibro(libro.libro_id)
        this.success = 'Libro eliminado con éxito'
        await this.loadLibros()
        this.clearMessages()
      } catch (error) {
        console.error('Error eliminando libro:', error)
        this.error = 'Error al eliminar el libro'
        this.clearMessages()
      }
    },
    
    async saveLibro() {
      if (!this.currentLibro.titulo.trim()) {
        this.error = 'El título es requerido'
        this.clearMessages()
        return
      }
      
      if (this.currentLibro.autores_ids.length === 0) {
        this.error = 'Debe seleccionar al menos un autor'
        this.clearMessages()
        return
      }
      
      this.loadingAction = true
      this.error = ''
      
      try {
        if (this.isEditing) {
          await api.updateLibro(this.currentLibro)
          this.success = 'Libro actualizado con éxito'
        } else {
          await api.createLibro(this.currentLibro)
          this.success = 'Libro creado con éxito'
        }
        
        this.closeModal()
        await this.loadLibros()
        this.clearMessages()
      } catch (error) {
        console.error('Error guardando libro:', error)
        this.error = error.response?.data?.error || 'Error al guardar el libro'
        this.clearMessages()
      } finally {
        this.loadingAction = false
      }
    },
    
    closeModal() {
      this.showModal = false
      this.isEditing = false
      this.currentLibro = {
        libro_id: null,
        titulo: '',
        anio_publicacion: null,
        autores_ids: [],
        generos_ids: []
      }
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