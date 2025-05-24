<template>
  <div class="container">
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">📖 Gestión de Libros</h2>
        <p class="card-subtitle">Administra los libros de la biblioteca</p>
      </div>
      
      <div style="margin-bottom: 20px;">
        <button @click="openNewLibroModal" class="btn btn-primary">
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
        <p v-if="!hasAutoresOrGeneros" style="margin-top: 10px; color: #666;">
          Para crear libros necesitas tener autores y géneros registrados.
          <router-link to="/autores" style="color: #667eea;">Ir a Autores</router-link> |
          <router-link to="/generos" style="color: #667eea;">Ir a Géneros</router-link>
        </p>
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
              <td>
                <strong>{{ libro.titulo }}</strong>
              </td>
              <td>{{ libro.anio_publicacion || 'N/A' }}</td>
              <td>
                <div v-if="libro.autores && libro.autores.length">
                  <span 
                    v-for="(autor, index) in libro.autores" 
                    :key="autor.autor_id"
                    class="autor-tag"
                  >
                    {{ autor.nombre }} {{ autor.apellido }}
                    <span v-if="index < libro.autores.length - 1">, </span>
                  </span>
                </div>
                <span v-else style="color: #999; font-style: italic;">Sin autores</span>
              </td>
              <td>
                <div v-if="libro.generos && libro.generos.length">
                  <span 
                    v-for="(genero, index) in libro.generos" 
                    :key="genero.genero_id"
                    class="genero-tag"
                  >
                    {{ genero.nombre }}
                    <span v-if="index < libro.generos.length - 1">, </span>
                  </span>
                </div>
                <span v-else style="color: #999; font-style: italic;">Sin géneros</span>
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
    
    <!-- Componente de formulario para crear/editar libro -->
    <LibroForm
      v-if="showModal"
      :libro="selectedLibro"
      @close="closeModal"
      @saved="onLibroSaved"
    />
  </div>
</template>

<script>
import api from '@/services/api'
import LibroForm from './LibroForm.vue'

export default {
  name: 'LibroList',
  components: {
    LibroForm
  },
  data() {
    return {
      libros: [],
      showModal: false,
      selectedLibro: null, // null para nuevo libro, objeto para editar
      loading: false,
      error: '',
      success: '',
      hasAutoresOrGeneros: true
    }
  },
  async created() {
    await this.loadLibros()
    await this.checkRequiredData()
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
        this.error = 'Error al cargar los libros. Verifica la conexión con el servidor.'
      } finally {
        this.loading = false
      }
    },
    
    async checkRequiredData() {
      try {
        const [autoresResponse, generosResponse] = await Promise.all([
          api.getAutores(),
          api.getGeneros()
        ])
        
        const autores = autoresResponse.data || []
        const generos = generosResponse.data || []
        
        this.hasAutoresOrGeneros = autores.length > 0 && generos.length > 0
      } catch (error) {
        console.error('Error verificando datos requeridos:', error)
        this.hasAutoresOrGeneros = false
      }
    },
    
    openNewLibroModal() {
      if (!this.hasAutoresOrGeneros) {
        this.showErrorMessage('Necesitas tener autores y géneros registrados antes de crear un libro')
        return
      }
      this.selectedLibro = null
      this.showModal = true
    },
    
    editLibro(libro) {
      // Crear una copia profunda del libro para editar
      this.selectedLibro = {
        ...libro,
        autores: libro.autores ? [...libro.autores] : [],
        generos: libro.generos ? [...libro.generos] : []
      }
      this.showModal = true
    },
    
    async deleteLibro(libro) {
      if (!confirm(`¿Estás seguro de eliminar el libro "${libro.titulo}"?`)) {
        return
      }
      
      try {
        await api.deleteLibro(libro.libro_id)
        this.showSuccessMessage('Libro eliminado con éxito')
        await this.loadLibros()
      } catch (error) {
        console.error('Error eliminando libro:', error)
        
        // Manejo específico de errores
if (error.response && error.response.status === 404) {
          this.showErrorMessage('El libro no existe')
} else if (error.response && error.response.status === 400) {
this.showErrorMessage((error.response && error.response.data && error.response.data.error) || 'Error al eliminar el libro')
        } else {
          this.showErrorMessage('Error al eliminar el libro')
        }
      }
    },
    
    closeModal() {
      this.showModal = false
      this.selectedLibro = null
    },
    
    async onLibroSaved() {
      const message = this.selectedLibro ? 'Libro actualizado con éxito' : 'Libro creado con éxito'
      this.showSuccessMessage(message)
      await this.loadLibros()
    },
    
    showSuccessMessage(message) {
      this.success = message
      this.error = ''
      this.clearMessages()
    },
    
    showErrorMessage(message) {
      this.error = message
      this.success = ''
      this.clearMessages()
    },
    
    clearMessages() {
      setTimeout(() => {
        this.error = ''
        this.success = ''
      }, 5000)
    }
  }
}
</script>

<style scoped>
.autor-tag, .genero-tag {
  font-size: 0.9rem;
  color: #333;
}

.autor-tag {
  background-color: #e3f2fd;
  padding: 2px 6px;
  border-radius: 12px;
  margin: 2px;
  display: inline-block;
}

.genero-tag {
  background-color: #f3e5f5;
  padding: 2px 6px;
  border-radius: 12px;
  margin: 2px;
  display: inline-block;
}
</style>