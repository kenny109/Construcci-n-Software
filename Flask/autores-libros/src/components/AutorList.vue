<template>
  <div class="container">
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">📚 Gestión de Autores</h2>
        <p class="card-subtitle">Administra los autores de la biblioteca</p>
      </div>

      <div style="margin-bottom: 20px;">
        <button @click="openNewAutorModal" class="btn btn-primary">
          ➕ Nuevo Autor
        </button>
      </div>

      <!-- Buscador de libros por autor -->
      <div class="flex items-center space-x-2 mb-4">
        <input
          v-model="autorBusqueda"
          type="number"
          placeholder="ID del autor"
          class="input input-bordered w-1/3"
        />
        <button @click="buscarLibrosPorAutor" class="btn btn-secondary">
          🔍 Buscar libros
        </button>
      </div>

      <!-- Mostrar resultado de la búsqueda -->
      <div v-if="librosBuscados.length > 0" class="mb-4">
        <h3>📖 Libros del autor con ID {{ autorBusqueda }}:</h3>
        <ul class="list-disc list-inside">
          <li v-for="libro in librosBuscados" :key="libro.libro_id">
            {{ libro.titulo }}
          </li>
        </ul>
      </div>

      <div v-else-if="busquedaRealizada" class="mb-4">
        <p>No se encontraron libros para el autor con ID {{ autorBusqueda }}</p>
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

    <!-- Componente de formulario para crear/editar autor -->
    <AutorForm
      v-if="showModal"
      :autor="selectedAutor"
      @close="closeModal"
      @saved="onAutorSaved"
    />
  </div>
</template>

<script>
import api from '@/services/api'
import AutorForm from './AutorForm.vue'
import '@/assets/styles.css'

export default {
  name: 'AutorList',
  components: {
    AutorForm
  },
  data() {
    return {
      autores: [],
      librosPorAutor: {},
      showModal: false,
      selectedAutor: null,
      loading: false,
      error: '',
      success: '',
      autorBusqueda: '',
      librosBuscados: [],
      busquedaRealizada: false
    }
  },
  async created() {
    await this.loadAutores()
  },
  methods: {
    async loadAutores() {
      this.loading = true
      this.error = ''
      this.librosPorAutor = {}

      try {
        const response = await api.getAutores()
        this.autores = response.data || []

        for (const autor of this.autores) {
          try {
            const librosResp = await api.getLibrosPorAutor(autor.autor_id)
            this.librosPorAutor[autor.autor_id] = librosResp.data || []
          } catch (e) {
            console.warn(`No se pudieron cargar los libros del autor ${autor.autor_id}`)
            this.librosPorAutor[autor.autor_id] = []
          }
        }
      } catch (error) {
        console.error('Error cargando autores:', error)
        this.error = 'Error al cargar los autores. Verifica la conexión con el servidor.'
      } finally {
        this.loading = false
      }
    },

    async buscarLibrosPorAutor() {
      this.librosBuscados = []
      this.busquedaRealizada = false

      if (!this.autorBusqueda) {
        this.showErrorMessage('Por favor ingresa un ID de autor')
        return
      }

      try {
        const resp = await api.getLibrosByAutor(this.autorBusqueda)
        this.librosBuscados = resp.data || []
      } catch (error) {
        console.error('Error buscando libros por autor:', error)
        this.showErrorMessage('Error al buscar los libros del autor')
      } finally {
        this.busquedaRealizada = true
      }
    },

    openNewAutorModal() {
      this.selectedAutor = null
      this.showModal = true
    },

    editAutor(autor) {
      this.selectedAutor = { ...autor }
      this.showModal = true
    },

    async deleteAutor(autor) {
      if (!confirm(`¿Estás seguro de eliminar al autor ${autor.nombre} ${autor.apellido}?`)) {
        return
      }

      try {
        await api.deleteAutor(autor.autor_id)
        this.showSuccessMessage('Autor eliminado con éxito')
        await this.loadAutores()
      } catch (error) {
        console.error('Error eliminando autor:', error)

        if (error.response && error.response.status === 400) {
          this.showErrorMessage('No se puede eliminar el autor porque tiene libros asociados')
        } else if (error.response && error.response.status === 404) {
          this.showErrorMessage('El autor no existe')
        } else {
          this.showErrorMessage('Error al eliminar el autor')
        }
      }
    },

    closeModal() {
      this.showModal = false
      this.selectedAutor = null
    },

    async onAutorSaved() {
      const message = this.selectedAutor ? 'Autor actualizado con éxito' : 'Autor creado con éxito'
      this.showSuccessMessage(message)
      await this.loadAutores()
    },

    formatDate(dateString) {
      if (!dateString) return 'No especificada'
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('es-ES', {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        })
      } catch (error) {
        return 'Fecha inválida'
      }
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
