<template>
  <div class="container">
    <div class="card">
      <div class="card-header">
        <h2 class="card-title">🏷️ Gestión de Géneros</h2>
        <p class="card-subtitle">Administra los géneros literarios</p>
      </div>

      <div class="form-actions" style="margin-bottom: 25px;">
        <button @click="showModal = true" class="btn btn-primary">
          ➕ Nuevo Género
        </button>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Cargando géneros...</p>
      </div>

      <div v-else-if="error" class="alert alert-error">
        {{ error }}
      </div>

      <div v-else-if="generos.length === 0" class="alert alert-warning">
        No hay géneros registrados. ¡Crea el primero!
      </div>

      <div v-else class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="genero in generos" :key="genero.genero_id">
              <td>{{ genero.genero_id }}</td>
              <td>{{ genero.nombre }}</td>
              <td>
                <button 
                  @click="editGenero(genero)" 
                  class="btn btn-warning btn-sm"
                  style="margin-right: 10px;"
                >
                  ✏️ Editar
                </button>
                <button 
                  @click="deleteGenero(genero.genero_id)" 
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

    <!-- Modal para crear/editar género -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">
            {{ editingGenero ? 'Editar Género' : 'Nuevo Género' }}
          </h3>
          <button @click="closeModal" class="modal-close">✕</button>
        </div>

        <div v-if="modalError" class="alert alert-error">
          {{ modalError }}
        </div>

        <form @submit.prevent="saveGenero">
          <div class="form-group">
            <label class="form-label">Nombre del Género:</label>
            <input 
              v-model="generoForm.nombre"
              type="text" 
              class="form-input"
              placeholder="Ej: Ficción, Drama, Ciencia Ficción"
              required
              maxlength="100"
            >
          </div>

          <div class="modal-footer">
            <button type="button" @click="closeModal" class="btn btn-secondary">
              Cancelar
            </button>
            <button 
              type="submit" 
              class="btn btn-success"
              :disabled="modalLoading"
            >
              {{ modalLoading ? 'Guardando...' : (editingGenero ? 'Actualizar' : 'Crear') }}
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
  name: 'GeneroList',
  data() {
    return {
      generos: [],
      loading: false,
      error: '',
      showModal: false,
      editingGenero: null,
      modalError: '',
      modalLoading: false,
      generoForm: {
        nombre: ''
      }
    }
  },
  async created() {
    await this.loadGeneros()
  },
  methods: {
    async loadGeneros() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await api.getGeneros()
        this.generos = response.data
      } catch (error) {
        console.error('Error al cargar géneros:', error)
        this.error = 'Error al cargar la lista de géneros'
      } finally {
        this.loading = false
      }
    },

    editGenero(genero) {
      this.editingGenero = genero.genero_id
      this.generoForm = {
        nombre: genero.nombre
      }
      this.showModal = true
    },

    async saveGenero() {
      if (!this.generoForm.nombre.trim()) {
        this.modalError = 'El nombre del género es requerido'
        return
      }

      this.modalLoading = true
      this.modalError = ''

      try {
        if (this.editingGenero) {
          // Actualizar género existente
          const data = {
            genero_id: this.editingGenero,
            nombre: this.generoForm.nombre.trim()
          }
          await api.updateGenero(data)
        } else {
          // Crear nuevo género
          const data = {
            nombre: this.generoForm.nombre.trim()
          }
          await api.createGenero(data)
        }
        
        await this.loadGeneros()
        this.closeModal()
      } catch (error) {
        console.error('Error al guardar género:', error)
        this.modalError = (error.response && error.response.data && error.response.data.error) || 'Error al guardar el género'
      } finally {
        this.modalLoading = false
      }
    },

    async deleteGenero(generoId) {
      if (!confirm('¿Estás seguro de que quieres eliminar este género?')) {
        return
      }

      try {
        await api.deleteGenero(generoId)
        await this.loadGeneros()
      } catch (error) {
        console.error('Error al eliminar género:', error)
        this.error = (error.response && error.response.data && error.response.data.error) || 'Error al eliminar el género'
      }
    },

    closeModal() {
      this.showModal = false
      this.editingGenero = null
      this.modalError = ''
      this.generoForm = {
        nombre: ''
      }
    }
  }
}
</script>